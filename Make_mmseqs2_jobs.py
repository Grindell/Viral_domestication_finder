#!/usr/bin/python
import pandas as pd
import numpy as np
import sys 
import argparse
import os
import subprocess


# Print out a message when the program is initiated.
print('----------------------------------------------------------------\n')
print('                        MMseqs2_job_maker.\n')
print('----------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allow to make mmseqs jobs for slurm')
parser.add_argument("-i", "--species_name_file", help="introduce the txt file with species names")
parser.add_argument("-t", "--species_type", help="introduce the name of db species types, ex: Virus or Hymenoptera")
parser.add_argument("-db", "--data_base", help="introduce the name of file of the diamond prot db in .dmnd format") 
parser.add_argument("-o", "--out",help="The ouptut path where to create the slurm files")
parser.add_argument("-p", "--path",help="The path where to find the file Project")
args = parser.parse_args()


#python3 Make_mmseqs2_jobs.py -i /beegfs/data/bguinet/these/Species_genome_names.txt -t virus -db /beegfs/data/bguinet/these/NCBI_protein_viruses/mmseqs2_viral_db -o /beegfs/home/bguinet/these_scripts/Mmseqs2_jobs -p /beegfs/data/bguinet/these 


# Variable that stores fasta sequences
Species_name_file=args.species_name_file
Type_species=args.species_type
Data_base=args.data_base
Output_path=args.out
path=args.path

#Allow to get a letter to know where to take and save the files
if Type_species == "virus":
    Type_species = "V"
if Type_species == "Virus":
    Type_species = "V"
if Type_species == "Hymenoptera":
    Type_species = "H"
if Type_species == "hymenoptera":
    Type_species = "H"



num_species = sum(1 for line in open(Species_name_file)) # count number of lines in the file in order to now the number of decimals / by the first number given
list_of_names1=[]
for names in open(Species_name_file,"r"):
	list_of_names1.append(names)

list_of_names2=[]

for names in list_of_names1:
	list_of_names2.append(names.replace("\n", ""))
os.chdir(Output_path)

#   jobname = str(os.path.splitext(sys.argv[2])[0])
filecount = 1
#   numcmds = int(sys.argv[1])
#   line = cmds.readline()
if Type_species == "H":
    for names in list_of_names2:

            w = open("Busco_mmseqs2_job_"+str(names)+".sh",'w')
            w.write("#!/bin/bash\n")
            w.write("#SBATCH --cpus-per-task=10\n")
            w.write("#SBATCH --mem 5G\n")
            w.write("#SBATCH --constraint=haswell\n")
            w.write("#SBATCH -t 24:00:00\n")
            w.write("#SBATCH -e "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/Busco_mmseqs2_job.log/Busco_mmseqs2_job.error\n")
            w.write("#SBATCH -o "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/Busco_mmseqs2_job.log/Busco_mmseqs2_job.out\n")
            w.write("#SBATCH -J Busco_mmseqs2_job_"+str(names)+"\n")
            w.write("#SBATCH --mail-type=ALL\n")
            w.write("#SBATCH --mail-user=benjamin.guinet95@gmail.com\n")
            w.write("date;hostname;pwd\n")
            w.write("mmseqs2=/beegfs/data/bguinet/TOOLS/MMseqs2/build/bin/mmseqs\n")
            w.write("$mmseqs2 createdb\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_busco/run_BUSCO_v3/compiled_busco_aa\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_busco/run_BUSCO_v3/"+str(names)+"_mmseqs2_busco_db\n")
            w.write("$mmseqs2 createdb\\\n")
            w.write(path+"/Genomes/"+str(names)+"/"+str(names)+".fa\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/"+str(names)+"_mmseqs2_db\n")
            w.write("$mmseqs2 search\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/"+str(names)+"_mmseqs2_db\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_busco/run_BUSCO_v3/"+str(names)+"_mmseqs2_busco_db\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/result_mmseqs2\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/tpm -a -s 7.5 -e 0.01 --threads 10\n")
            w.write('$mmseqs2 convertalis --format-output "query,tlen,target,pident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits"\\\n')
            w.write(path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/"+str(names)+"_mmseqs2_db\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_busco/run_BUSCO_v3/"+str(names)+"_mmseqs2_busco_db\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/result_mmseqs2\\\n")
            w.write(path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/result_mmseqs2.m8\n")
            w.write("date")
            w.close()

            filled_len = int(round(50 * filecount / float(num_species-1)))
            percents = round(100.0 * filecount / float(num_species), 1)
            bar = '=' * filled_len + '-' * ((50) - filled_len)

            sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', ''))
            sys.stdout.flush()  # As suggested by Rom Ruben

            filecount += 1
        
if Type_species == "V":
    for names in list_of_names2:
            w = open("Viral_mmseqs2_job_"+str(names)+".sh",'w')
            w.write("#!/bin/bash\n")
            w.write("#SBATCH --cpus-per-task=10\n")
            w.write("#SBATCH --mem 5G\n")
            w.write("#SBATCH --constraint=haswell\n")
            w.write("#SBATCH -t 24:00:00\n")
            w.write("#SBATCH -e "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/Viral_mmseqs2_job.log/Viral_mmseqs2_job.error\n")
            w.write("#SBATCH -o "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/Viral_mmseqs2_job.log/Viral_mmseqs2_job.out\n")
            w.write("#SBATCH -J Viral_mmseqs2_job_"+str(names)+"\n")
            w.write("#SBATCH --mail-type=ALL\n")
            w.write("#SBATCH --mail-user=benjamin.guinet95@gmail.com\n")
            w.write("date;hostname;pwd\n")
            w.write("mmseqs2=/beegfs/data/bguinet/TOOLS/MMseqs2/build/bin/mmseqs\n")
            w.write("$mmseqs2 createdb\\\n")
            w.write(" "+path+"/Genomes/"+str(names)+"/"+str(names)+".fa\\\n")
            w.write(" "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/"+str(names)+"_mmseqs2_db\n")
            w.write("$mmseqs2 search\\\n")
            w.write(" "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/"+str(names)+"_mmseqs2_db\\\n")
            w.write(" "+Data_base+"\\\n")
            w.write(" "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/result_mmseqs2\\\n")
            w.write(" "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/tpm -a -s 7.5 -e 0.01 --threads 10\n")
            w.write('$mmseqs2 convertalis --format-output "query,tlen,target,pident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits"\\\n')
            w.write(" "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/"+str(names)+"_mmseqs2_db\\\n")
            w.write(" "+Data_base+"\\\n")
            w.write(" "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/result_mmseqs2\\\n")
            w.write(" "+path+"/Genomes/"+str(names)+"/run_mmseqs2_"+Type_species+"/result_mmseqs2.m8\n")
            w.write("date")
            w.close()


            filled_len = int(round(50 * filecount / float(num_species-1)))
            percents = round(100.0 * filecount / float(num_species), 1)
            bar = '=' * filled_len + '-' * ((50) - filled_len)

            sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', ''))
            sys.stdout.flush()  # As suggested by Rom Ruben

            filecount += 1

if Type_species != "H" and Type_species != "V": 
    print("Wrong type of species-type given")
    print("Please choose one of these one:")
    print("virus, Virus, Hymenoptera or hymenoptera")
    print("if the species type changes, please edit the Make_job_mmseqs2.py file in order to fit your own data")
