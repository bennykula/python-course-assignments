#!/usr/bin/env python3
"""Check inserted sequence between restriction sites by aligning PCR reads to plasmid.

Usage: python check_insertion.py --plasmid ROZMAN_D6Y_1_lentiv2_zim3_pLann.dna \
    --pcr 4212_100_1-guideRNAseqF.fasta --enzyme BsmBI --insert "CGGCGGCCCGCTCGCTCGGG"
"""
import argparse
import sys
from pathlib import Path

from Bio import Restriction
from Bio import SeqIO, pairwise2
from Bio.Seq import Seq
from Bio.Restriction import Restriction_Dictionary


def read_fasta_seq(path):
    recs = list(SeqIO.parse(path, "fasta"))
    if not recs:
        raise SystemExit(f"No sequences found in {path}")
    # return concatenated sequence if multiple
    return str(recs[0].seq).upper()


def read_dna_file(path):
    record = SeqIO.read(path, "snapgene")
    return str(record.seq).upper()


def rc(s):
    return str(Seq(s).reverse_complement())


def normalize_enzyme_name(name):
    return ''.join(ch for ch in name.lower() if ch.isalnum())


def resolve_enzyme(enzyme_name):
    requested_name = enzyme_name.strip()
    if requested_name in Restriction_Dictionary.rest_dict:
        library_name = requested_name
    else:
        normalized_requested = normalize_enzyme_name(requested_name)
        matches = [
            name for name in Restriction_Dictionary.rest_dict
            if normalize_enzyme_name(name) == normalized_requested
        ]

        if not matches:
            raise SystemExit(
                f"Could not determine recognition sequence for enzyme '{enzyme_name}'.\n"
                "This script uses Biopython's restriction library for enzyme lookup."
            )

        library_name = sorted(matches, key=lambda name: (name != requested_name, name))[0]

    if library_name not in Restriction_Dictionary.rest_dict:
        raise SystemExit(
            f"Could not determine recognition sequence for enzyme '{enzyme_name}'.\n"
            "This script uses Biopython's restriction library for enzyme lookup."
        )

    enzyme_cls = getattr(Restriction, library_name, None)
    if enzyme_cls is None:
        raise SystemExit(
            f"Biopython knows enzyme '{library_name}', but it is not available as a restriction class."
        )

    recog = Restriction_Dictionary.rest_dict[library_name]['site'].upper()
    return library_name, enzyme_cls, recog


def find_restriction_cut_positions(enzyme_cls, plasmid_seq):
    return list(enzyme_cls.search(Seq(plasmid_seq)))


def build_alignment_map(aligned_plasmid, aligned_pcr):
    mapping = {}
    plasmid_index = -1
    pcr_index = -1

    for aligned_plasmid_base, aligned_pcr_base in zip(aligned_plasmid, aligned_pcr):
        if aligned_plasmid_base != '-':
            plasmid_index += 1
        if aligned_pcr_base != '-':
            pcr_index += 1
            mapping[pcr_index] = plasmid_index if aligned_plasmid_base != '-' else None

    return mapping


def align_pcr_to_plasmid(plasmid_seq, pcr_seq):
    # local alignment: plasmid as seqA, pcr_seq as seqB
    aln = pairwise2.align.localms(plasmid_seq, pcr_seq, 2, -1, -0.5, -0.1)
    if not aln:
        return None
    best = aln[0]
    # best: (aligned_seqA, aligned_seqB, score, begin, end)
    return best


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--plasmid', required=True)
    p.add_argument('--pcr', required=True)
    p.add_argument('--enzyme', required=True)
    p.add_argument('--insert', required=True)
    args = p.parse_args()

    plasmid_path = Path(args.plasmid)
    pcr_path = Path(args.pcr)
    if not plasmid_path.exists():
        raise SystemExit(f"Plasmid file not found: {plasmid_path}")
    if not pcr_path.exists():
        raise SystemExit(f"PCR file not found: {pcr_path}")

    print(f"Reading plasmid from {plasmid_path}")
    plasmid_seq = read_dna_file(plasmid_path)
    print(f"Plasmid length: {len(plasmid_seq)}")

    print(f"Reading PCR reads from {pcr_path}")
    pcr_seq = read_fasta_seq(pcr_path)
    print(f"PCR read length: {len(pcr_seq)}")

    print(f"Resolving enzyme {args.enzyme}")
    library_name, enzyme_cls, recog = resolve_enzyme(args.enzyme)
    print(f"Recognition sequence: {recog}")
    cut_positions = find_restriction_cut_positions(enzyme_cls, plasmid_seq)
    print(f"Found {len(cut_positions)} restriction cut position(s) at positions: {cut_positions}")

    print("Aligning PCR read to plasmid (local alignment)")
    aln = align_pcr_to_plasmid(plasmid_seq, pcr_seq)
    if aln is None:
        print("No alignment found between PCR read and plasmid.")
        sys.exit(2)
    aligned_plasmid, aligned_pcr, score, begin, end = aln
    print(f"Best alignment in plasmid: start={begin} end={end} (0-based, end exclusive), score={score}")

    alignment_map = build_alignment_map(aligned_plasmid, aligned_pcr)

    insert = args.insert.upper()
    print(f"Inserted sequence provided: {insert}")
    insert_in_read = pcr_seq.find(insert)
    insert_sequence = insert
    if insert_in_read == -1:
        insert_in_read = pcr_seq.find(rc(insert))
        insert_sequence = rc(insert)

    if insert_in_read == -1:
        print("Could not find the exact insert sequence in the PCR read.")
        sys.exit(3)

    insert_end = insert_in_read + len(insert_sequence)
    insert_plasmid_positions = [
        alignment_map[idx]
        for idx in range(insert_in_read, insert_end)
        if alignment_map.get(idx) is not None
    ]

    if insert_plasmid_positions:
        insert_span = (min(insert_plasmid_positions), max(insert_plasmid_positions))
        print(f"Insert maps to plasmid span: {insert_span[0]}-{insert_span[1]}")
    else:
        insert_span = None
        print("Insert does not map to any plasmid coordinates in the alignment.")

    cut_tolerance = 10
    insert_touches_cut = False
    if insert_span is not None:
        insert_start, insert_stop = insert_span
        insert_touches_cut = any(
            abs(cut - insert_start) <= cut_tolerance or abs(cut - insert_stop) <= cut_tolerance
            for cut in cut_positions
        )
        print(f"Insert touches a restriction cut: {insert_touches_cut}")

    success = insert_span is not None and insert_touches_cut
    if success:
        print("SUCCESS: Insert appears present and aligned between restriction sites.")
        sys.exit(0)
    else:
        print("FAIL: Insert not detected as expected between restriction sites.")
        sys.exit(3)


if __name__ == '__main__':
    main()
