#!/usr/bin/python
import pandas as pd
import numpy as np
import sys 

import argparse
import os

# Print out a message when the program is initiated.
print('----------------------------------------------------------------\n')
print('                        Create BED file.\n')
print('----------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allows to create a bed file from a  dataframe')
parser.add_argument("-i", "--table", help="introduce the Matches-species_without_overlapping.txt file")
parser.add_argument("-o", "--out", help="introduce the desired output name")

args = parser.parse_args()


# Variable that stores fasta sequences
Table=args.table
Output_file=args.out

blast=pd.read_table(Table,sep=" ")
blast=blast.drop(["width","numbers","type"],axis=1)
blast["name"]="Species"
blast["number"]="0"
blast= blast[['seqnames', 'start', 'end','name', 'number', 'strand']]
#When the strand is minus, then add 2 nucleotides at the end in order to have the good reading frame. 
blast[['start','end']]=np.where(blast['strand'].eq('-')[:,None],np.column_stack((blast['start']+0,blast['end']-2)),blast[['start','end']].values)
blast.to_csv(Output_file,sep='\t',index= False,header=False)
print("Bed file completed")
print("Output written at: ", Output_file)



#Here is a command line in bash in order to get BED file for a list of species:
#cat short_file_species_name.txt | while read line; do python3 Create_bed_file.py --table /beegfs/data/bguinet/M2/${line}/Matches_${line}_without_overlapping_sequence
s.txt --out /beegfs/data/bguinet/M2/${line}/Recover_fasta_loci.bed
