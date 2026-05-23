# Day 06 - RCSB PDB Query

This program queries the RCSB Protein Data Bank (PDB), a web-based database of
3D biomolecular structures (proteins, nucleic acids, complexes) and associated
metadata such as experimental methods, resolutions, and release dates.

The script performs a full-text search in the PDB and then downloads metadata
for the top matching structures. It summarizes the results by experimental
method, resolution, and release year.

## Requirements

- Python 3
- `pypdb` (see `requirements.txt`)

## Usage

From the repository root:

```bash
python day06/pdb_query.py --query "Cas9" --top 10
```

You can change the query to any keyword (e.g. `ribosome`, `hemoglobin`,
`CRISPR`). The `--top` argument limits how many entries are downloaded.

## Notes

- The script uses the PyPDB library, which wraps the official RCSB PDB APIs.
- No web scraping or manual HTTP requests are used.

## Implementation

The program uses the `pypdb` Python package, a lightweight wrapper around the
RCSB PDB API. The implementation is intentionally simple and focused on
demonstrating a typical workflow:

- Build a full-text search operator using `pypdb.clients.search.operators`.
- Execute the search with `pypdb.clients.search.search_client.perform_search`.
- Create a `DataFetcher` for the top matching entry IDs and request a small
	set of properties (`struct.title`, `exptl.method`, `rcsb_entry_info.resolution_combined`,
	`rcsb_accession_info.initial_release_date`).
- Convert the fetched data to a flattened dictionary and print a compact
	table of ID / method / resolution / release date / title, followed by a
	short summary (average resolution, counts by method and release year).

The source code is `pdb_query.py` in this directory. The code avoids raw
HTTP requests and scraping by relying solely on the official APIs surfaced
through `pypdb`.

## AI interaction

I used GitHub Copilot in VS Code to accelerate development. The AI helped with
writing the CLI glue code and data normalization utilities; I reviewed and
edited the resulting code to keep the implementation simple, readable, and
robust.

Original goal: implement a CLI that searches the PDB by keyword, downloads
metadata for the top N results, and summarizes methods, resolutions, and
release years.
