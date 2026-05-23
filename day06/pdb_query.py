#!/usr/bin/env python3
"""Query the RCSB Protein Data Bank (PDB) and summarize matching entries.

Example:
    python day06/pdb_query.py --query "Cas9" --top 10
"""

from __future__ import annotations

import argparse
from collections import Counter
from textwrap import shorten

from pypdb.clients.data.data_types import DataFetcher, DataType
from pypdb.clients.search.operators import text_operators
from pypdb.clients.search.search_client import RequestOptions, ReturnType, perform_search
import requests


def search_entries(query: str, top_n: int) -> list[str]:
    operator = text_operators.DefaultOperator(value=query)
    request_options = RequestOptions(
        result_start_index=0,
        num_results=top_n,
        sort_by="score",
        desc=True,
    )
    try:
        results = perform_search(
            search_operator=operator,
            return_type=ReturnType.ENTRY,
            request_options=request_options,
            verbosity=False,
        )
    except requests.exceptions.JSONDecodeError:
        # API returned a non-JSON or empty response (e.g. no results); treat as no hits
        return []
    except requests.exceptions.RequestException as exc:
        # Network or HTTP error from requests
        print(f"PDB search request failed: {exc}")
        return []
    except Exception as exc:
        # Any other unexpected error from the library
        print(f"PDB search failed: {exc}")
        return []

    if not results:
        return []

    return list(results)


def fetch_entry_data(entry_ids: list[str]) -> dict:
    fetcher = DataFetcher(entry_ids, DataType.ENTRY)
    fetcher.add_property(
        {
            "struct": ["title"],
            "exptl": ["method"],
            "rcsb_entry_info": ["resolution_combined"],
            "rcsb_accession_info": ["initial_release_date"],
        }
    )
    fetcher.fetch_data()
    return fetcher.return_data_as_df_dict() or {}


def normalize_method(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value


def normalize_title(value):
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


def normalize_resolution(value):
    if isinstance(value, list):
        for item in value:
            try:
                return float(item)
            except (TypeError, ValueError):
                continue
        return None
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_year(date_value):
    if not date_value:
        return None
    if isinstance(date_value, list):
        date_value = date_value[0] if date_value else None
    if not date_value:
        return None
    year = str(date_value)[:4]
    return int(year) if year.isdigit() else None


def print_summary(rows, resolutions, method_counts, year_counts):
    print("\nSummary")
    print("-" * 70)
    if resolutions:
        avg_res = sum(resolutions) / len(resolutions)
        print(f"Average resolution: {avg_res:.2f} A (n={len(resolutions)})")
    else:
        print("Average resolution: n/a")

    if method_counts:
        print("Methods:")
        for method, count in method_counts.most_common():
            print(f"  {method}: {count}")
    else:
        print("Methods: n/a")

    if year_counts:
        print("Release years:")
        for year, count in year_counts.most_common():
            print(f"  {year}: {count}")
    else:
        print("Release years: n/a")

    if rows:
        print("\nEntries listed:")
        for row in rows:
            print(f"  {row}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search the RCSB PDB and summarize matching structures."
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Full-text query (e.g. 'Cas9', 'ribosome', 'hemoglobin').",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Maximum number of entries to fetch (default: 10).",
    )
    args = parser.parse_args()

    if args.top <= 0:
        raise SystemExit("--top must be a positive integer")

    entry_ids = search_entries(args.query, args.top)
    if not entry_ids:
        print("No PDB entries found for the given query.")
        return 1

    data = fetch_entry_data(entry_ids)

    print(f"Found {len(entry_ids)} PDB entries for query: {args.query}")
    print("ID     | Method                   | Res (A) | Release    | Title")
    print("-" * 90)

    resolutions = []
    method_counts = Counter()
    year_counts = Counter()
    rows = []

    for entry_id in entry_ids:
        entry = data.get(entry_id, {})
        method = normalize_method(entry.get("exptl.method")) or "n/a"
        title = normalize_title(entry.get("struct.title"))
        resolution = normalize_resolution(entry.get("rcsb_entry_info.resolution_combined"))
        release_date = entry.get("rcsb_accession_info.initial_release_date")

        res_display = f"{resolution:.2f}" if resolution is not None else "n/a"
        date_display = str(release_date)[:10] if release_date else "n/a"
        title_display = shorten(title, width=60, placeholder="...")

        method_counts[method] += 1
        if resolution is not None:
            resolutions.append(resolution)
        year = extract_year(release_date)
        if year is not None:
            year_counts[year] += 1

        print(
            f"{entry_id:6} | {shorten(method, width=22, placeholder='...'):22} "
            f"| {res_display:>7} | {date_display:10} | {title_display}"
        )
        rows.append(entry_id)

    print_summary(rows, resolutions, method_counts, year_counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
