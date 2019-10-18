#!/usr/bin/env python

import sys
from Bio import SeqIO
import argparse

print('-----------------------------------------------------------------------------------\n')
print('                        Purge a fasta file of contamination sequences.\n')
print('-----------------------------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allow add taxonomy informationsa blast file')
parser.add_argument("-c","--ID_conta_file", help="The file with the IDs of contamination sequences")
parser.add_argument("-f","--fasta_file", help="The fasta file with all sequences")
parser.add_argument("-o","--out", help="The oufile without contamination")
args = parser.parse_args()


#Usage exemple
"""
Purge_fasta_file_from_conta.py -c /beegfs/data/bguinet/these/NCBI_protein_viruses/All_phages_and_polydnaviridae_families_conta.txt -f /beegfs/data/bguinet/these/NCBI_protein_viruses/All_viral_protein_sequences.fa -o /beegfs/data/bguinet/these/NCBI_protein_viruses/All_viral_protein_sequences_without_contamination.fa
"""

Conta_ids=args.ID_conta_file
Fasta_file=args.fasta_file
Outfile=args.out


identifiers = set([])

with open(Conta_ids, 'r') as fi:
    for line in fi:
        line = line.strip()
        #Only keep only the part before the .x in seq id:
        line = line.split(".", 1)[0]
        identifiers.add(str(line).replace(">", ""))


with open(Fasta_file) as original_fasta, open(Outfile, 'w') as corrected_fasta:
    records = SeqIO.parse(original_fasta, 'fasta')
    for record in records:
        if record.id not in identifiers:
            SeqIO.write(record, corrected_fasta, 'fasta')
	   
	   
print ("All sequences without contamination have been printed here", Outfile)
