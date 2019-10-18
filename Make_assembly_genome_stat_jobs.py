#!/usr/bin/python
import sys 
import argparse
import os
import subprocess
# Print out a message when the program is initiated.
print('----------------------------------------------------------------\n')
print('                        Assembly_stats_job_maker.\n')
print('----------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allow to make assembly jobs with QUAST for slurm')
parser.add_argument("-i", "--species_name_file", help="introduce the txt file with species names")
parser.add_argument("-p", "--path",help="The path where to find the file Project")
args = parser.parse_args()


#Exemple usage : 

#python3 Make_assembly_genome_stat_jobs.py -i /beegfs/data/bguinet/these/Species_genome_names.txt -p /beegfs/data/bguinet/these
# Variable that stores fasta sequences
Species_name_file=args.species_name_file
path=args.path


num_species = sum(1 for line in open(Species_name_file)) # count number of lines in the file in order to know the number of decimals / by the first number given
list_of_names1=[]
for names in open(Species_name_file,"r"):
	list_of_names1.append(names)
list_of_names2=[]
for names in list_of_names1:
	list_of_names2.append(names.replace("\n", ""))
filecount = 1

for names in list_of_names2:
		w = open("Assembly_stat_job_"+str(names)+".sh",'w')
		w.write("#!/bin/bash\n")
		w.write("mkdir "+path+"/Genomes/"+str(names)+"/Genome_assembly_statistics\n")
		w.write("#SBATCH -t 1:00:00\n")
		w.write("#SBATCH --cpus-per-task=4")
		w.write("#SBATCH -e "+path+"/Genomes/"+str(names)+"/Genome_assembly_statistics/Assembly_stat_job.error\n")
		w.write("#SBATCH -o "+path+"/Genomes/"+str(names)+"/Genome_assembly_statistics/Assembly_stat_job.out\n")
		w.write("#SBATCH -J Assembly_stat_job_"+str(names)+"\n")
		w.write("#SBATCH --mail-type=ALL\n")
		w.write("#SBATCH --mail-user=benjamin.guinet95@gmail.com\n")
		w.write("date;hostname;pwd\n")
		w.write("python3 /beegfs/data/bguinet/TOOLS/quast/quast.py "+path+"/Genomes/"+str(names)+"/"+str(names)+".fa -o "+path+"/Genomes/"+str(names)+"/Genome_assembly_statistics\n")
		w.close()

		filled_len = int(round(50 * filecount / float(num_species-1)))
		percents = round(100.0 * filecount / float(num_species), 1)
		bar = '=' * filled_len + '-' * ((50) - filled_len)

		sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', ''))
		sys.stdout.flush()  # As suggested by Rom Ruben

		filecount += 1
