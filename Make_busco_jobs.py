#!/usr/bin/python
import pandas as pd
import numpy as np
import sys 
import argparse
import os

# Print out a message when the program is initiated.
print('----------------------------------------------------------------\n')
print('                        Busco_job_maker.\n')
print('----------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allow to make busco jobs for slurm')
parser.add_argument("-i", "--species_name_file", help="introduce the .txt file with all the species names")
parser.add_argument("-o", "--out",help="The ouptut path where to create the slurm files")
parser.add_argument("-p", "--path",help="The path where to find the file Project")

args = parser.parse_args()

#Ex usage: python3 Make_busco_jobs.py -i /beegfs/home/bguinet/Species_genome_names.txt  -o $DIR/M2_script/Busco_jobs -p /beegfs/data/bguinet/

#This script allow you to create Busco_job.sh in order to run these scripts with slurm


# Variable that stores fasta sequences
Species_name_file=args.species_name_file
Output_path=args.out
path=args.path


num_species = sum(1 for line in open(Species_name_file)) # count number of lines in the file in order to now the number of decimals / by the first number given
list_of_names1=[]
for names in open(Species_name_file,"r"):
	list_of_names1.append(names)

list_of_names2=[]

for names in list_of_names1:
	list_of_names2.append(names.replace("\n", ""))
os.chdir(Output_path)


filecount = 1
for names in list_of_names2:
	w = open("Busco_job_"+str(names)+".sh",'w')
	w.write("#!/bin/bash\n")
	w.write("#SBATCH -t 64:00:00\n")
	w.write("#SBATCH --cpus-per-task=3\n")
	w.write("#SBATCH -e "+path+"Genomes/"+str(names)+"/run_busco/busco_job.log/busco_job.error\n")
	w.write("#SBATCH -o "+path+"Genomes/"+str(names)+"/run_busco/busco_job.log/busco_job.out\n")
	w.write("#SBATCH -J Genome_busco_job_"+str(names)+"\n")
	w.write("#SBATCH --mail-type=ALL\n")
	w.write("#SBATCH --mail-user=benjamin.guinet95@gmail.com\n") #<--------- the email where you desire to get the informations about the process running 
	w.write("date;hostname;pwd\n")
	w.write("ASSEMBLY="+path+"Genomes/"+str(names)+"/"+str(names)+".fa\n")
	w.write("LINEAGE=/beegfs/data/bguinet/these/Busco_Hymenoptera_database/\n") #<--------- the path where to find the lineage file 
	#w.write("NAME=/beegfs/data/bguinetGenomes/"+str(names)+"/run_busco/busco_v3_"+str(names)+"\n")
	w.write("SAMP="+str(names)+"\n")
	w.write("NAME=$SAMP'_BUSCO_v3'\n")
	w.write("#########################################\n")
	w.write("# define PATH to sofwtare used by BUSCO #\n")
	w.write("#########################################\n")
	w.write("#Augustus\n")
	w.write("export PATH=/bin:/usr/bin:/usr/remote/bin:/beegfs/data/bguinet/TOOLS/Augustus3.3/bin:/beegfs/data/bguinet/TOOLS/Augustus3.3/scripts\n") #<--------- the path where to find Augustus program
	#w.write("export PATH=/bin:/usr/bin:/usr/remote/bin:/beegfs/data/bguinet/TOOLS/Augustus3.3\n")
	w.write("# hmmer\n")
	w.write("PATH=$PATH:/beegfs/data/bguinet/TOOLS/hmmer-3.2.1/bin\n") #<--------- the path where to find hmmer program
	w.write("# blast et python\n")
	w.write("PATH=$PATH:/beegfs/data/bguinet/TOOLS/ncbi-blast-2.8.1+/bin\n") #<--------- the path where to find ncbi-blast program
	w.write("PATH=$PATH:/usr/bin\n")
	w.write("# augustus\n")
	w.write("export AUGUSTUS_CONFIG_PATH=/beegfs/data/bguinet/TOOLS/Augustus3.3/config\n")
	w.write("#Busco software path\n")
	w.write("BUSCO='/beegfs/data/bguinet/myconda/bin/run_BUSCO.py'\n") #<--------- the path where to find Busco program
	w.write("################\n")
	w.write("# Command line #\n")
	w.write("################\n")
	w.write("export PATH=/usr/remote/Python-3.6.5/bin:$PATH\n") #<--------- the path where to find the Python program
	w.write("PATH=$PATH:/usr/bin\n")
	w.write("cd "+path+"Genomes/"+str(names)+"/run_busco\n")
	w.write("export PYTHONPATH=$PYTHONPATH:/beegfs/data/bguinet/myconda/lib/python3.7/site-packages/\n")
	w.write("python3 $BUSCO -i $ASSEMBLY -o $NAME -l $LINEAGE -m geno -f\n")
	w.close()

	filled_len = int(round(50 * filecount / float(num_species-1)))
	percents = round(100.0 * filecount / float(num_species), 1)
	bar = '=' * filled_len + '-' * ((50) - filled_len)

	sys.stdout.write('[%s] %s%s finish%s\r' % (bar, percents, '%', ''))
	sys.stdout.flush()  # As suggested by Rom Ruben
	filecount += 1
print("\n")
print(filecount-1," files created at :",Output_path)
