import pandas as pd
import numpy as np
from pandas import DataFrame
import os
import sys
import argparse


# Print out a message when the program is initiated.
print('----------------------------------------------------------------\n')
print('                        Busco_summary.\n')
print('----------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allow to make busco jobs for slurm')
parser.add_argument("-i", "--species_name_file", help="introduce the .txt file with all the species names")
parser.add_argument("-o", "--out",help="The ouptut path where to create the slurm files")
parser.add_argument("-p", "--path",help="The path where to find the file Project")

args = parser.parse_args()

# Variable that stores fasta sequences
Species_name_file=args.species_name_file
Output_path=args.out
path=args.path

#Ex: python3 Busco_summary.py -i /beegfs/data/bguinet/these/Species_genome_names.txt  -o /beegfs/home/bguinet/these_scripts/Busco_jobs -p /beegfs/data/bguinet/these/


num_species = sum(1 for line in open(Species_name_file)) # count number of lines in the file in order to now the number of decimals / by the first number given
list_of_names1=[]
filecount = 1
for names in open(Species_name_file,"r"):
	list_of_names1.append(names)

list_of_names2=[]

for names in list_of_names1:
	list_of_names2.append(names.replace("\n", ""))
df2 = pd.DataFrame(columns=("Species",'Complete', 'Duplicated', 'Fragmented','Missing','Total'))

for names in list_of_names2:

	try:
		f=open(path+"Genomes/"+str(names)+"/run_busco/run_BUSCO_v3/full_table_"+str(names)+"_BUSCO_v3.tsv")
		lines = f.readlines()
		f.close()

		f = open('file.txt','w')
		f.write( "".join( lines[4:] ) )
		f.close()

		df1= pd.read_csv("file.txt",sep="\t")
		df1.columns = ["Busco id","Status", "Contig", "Start", "End", "Score", "Length"]


		df1= pd.read_csv("file.txt",sep="\t")
		df1.columns = ["Busco id","Status", "Contig", "Start", "End", "Score", "Length"]

		Number_Fragmented=(df1[df1["Status"].str.contains("Fragmented")==True].shape[0])
		Number_Missing=(df1[df1["Status"].str.contains("Missing")==True].shape[0])
		Number_Duplicated=(df1[df1["Status"].str.contains("Duplicated")==True].shape[0])
		Number_Complete=(df1[df1["Status"].str.contains("Complete")==True].shape[0])

		Number_complete_duplicated=Number_Complete+Number_Duplicated/2


		df2=df2.append({'Species':names,'Complete':int(Number_complete_duplicated),'Duplicated':int(Number_Duplicated/2), 'Fragmented':int(Number_Fragmented),'Missing':int(Number_Missing),'Total':4415}, ignore_index=True)


		df2.to_csv(Output_path,sep='\t')
	
	except OSError as e:
		print(names,"did not pass")

print(df2)
