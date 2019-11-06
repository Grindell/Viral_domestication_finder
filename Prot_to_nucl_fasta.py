#!/usr/bin/python
import sys 
from Bio import SeqIO
from Bio import Entrez
import re
import argparse
import os

# Print out a message when the program is initiated.
print('---------------------------------------------------------------------------\n')
print('                 Recover nucleotide fasta seq from protein ids file.       \n')
print('---------------------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allows to create a bed file from a  dataframe')
parser.add_argument("-i", "--ids_table", help="The txt file with all the protein seq ids (one/line)")
parser.add_argument("-o", "--out", help="introduce the desired output name file")

args = parser.parse_args()

# Variable that stores fasta sequences
Table=args.table
Output_file=args.out

num_ids = sum(1 for line in open(Table)) # count number of lines in the file in order to now the number of decimals / by the first number given
list_of_ids1=[]
for ids in open(Table,"r"):
	list_of_ids1.append(ids)

list_of_ids2=[]
for names in list_of_ids1:
	list_of_ids2.append(names.replace("\n", ""))

filecount = 1
Ids_file = open(Table, "r")
with open("example.fasta", "w") as output_handle:
	for id in Ids_file: 
		id = re.sub(r'\n', '', id)
		if "_CP_" in id: 
			id = id.split("_CP_", 1)[0]#Because some sequence have a tag.
		handle=Entrez.efetch(db="sequences", id=id, rettype="fasta_cds_na", retmode="text")
		record = SeqIO.read(handle, "fasta")
		#print("protein name :", id, "and nucleotide name :", record.id)
		#print(record)
		SeqIO.write(record , output_handle, "fasta")
		filled_len = int(round(50 * filecount / float(num_ids-1)))
		percents = round(100.0 * filecount / float(num_ids), 1)
		bar = '=' * filled_len + '-' * ((50) - filled_len)
		sys.stdout.write('[%s] %s%s finish%s\r' % (bar, percents, '%', ''))
		sys.stdout.flush()  # As suggested by Rom Ruben
		filecount += 1

print("All the nucleotides sequence have been printed to : ", Output_file)


