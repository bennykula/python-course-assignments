# check_insertion.py

This script validates a cloning result by comparing a PCR sequencing read against a plasmid `.dna`
file and checking whether the requested insert is supported by the selected restriction enzyme.

Requirements
- Python 3
- Biopython, see `requirements.txt`

Usage

From the repository root, run:

```bash
python day05/check_insertion.py \
  --plasmid day05/ROZMAN_D6Y_1_lentiv2_zim3_pLann.dna \
  --pcr day05/4212_100_1-guideRNAseqF/4212_100_1-guideRNAseqF.fasta \
  --enzyme BsmBI \
  --insert "CGGCGGCCCGCTCGCTCGGG"
```

Implementation details
- The plasmid `.dna` file is read with Biopython's `snapgene` parser.
- Restriction enzymes are resolved through Biopython's restriction database, so enzyme lookup is
  library-backed rather than hardcoded.
- The PCR read is aligned to the plasmid with a local alignment.
- The exact insert sequence is located in the PCR read.
- The alignment is used to map the insert bases back onto plasmid coordinates.
- The program succeeds only when the mapped insert span is close to one of the enzyme's actual cut
  positions in the plasmid.

Behavior
- If the requested enzyme is not found in the restriction library, the script exits with an error.
- If the exact insert sequence is not present in the PCR read, the script fails.
- If the mapped insert span does not line up with the selected enzyme's cut site, the script fails.

Notes
- `BsmbI`, `BsmBI`, and other library-recognized aliases are resolved through Biopython's
  restriction catalog.
- The sample data in this repository passes with `BsmBI` and the insert
  `CGGCGGCCCGCTCGCTCGGG`.
