#!/usr/bin/python
import pandas as pd
import numpy as np
import sys 
import argparse
from taxadb.taxid import TaxID
from taxadb.accessionid import AccessionID
import time


# Print out a message when the program is initiated.
print('-----------------------------------------------------------------------------------\n')
print('                        Add taxonomy informations into blast tab.\n')
print('-----------------------------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allow add taxonomy informationsa blast file')
parser.add_argument("-b", "--blast", help="The blast file in .m8 format (check the column names and modify the colname 'target' wich corresponds to the Acc_number column in the mmseqs2 software")
parser.add_argument("-o", "--out",help="The ouptut path where to create the oufile")
parser.add_argument("-d", "--taxadb_sqlite_file", help="The directory where is located the sqlite database")
args = parser.parse_args()

"""
Ex usage python3 add_taxid_info.py -b /beegfs/home/bguinet/M2_script/dataframe_brute.txt -d /beegfs/data/bguinet/taxadb.sqlite -o /beegfs/home/bguinet/M2_script/Out_file.m8 
"""

"""
Here are the steps to install the taxadb sqlite (from https://github.com/HadrienG/taxadb) 

1) Install the package taxadb :
>>> pip3 install taxadb

2) Create the SQlite database:

(In order to create your own database, you first need to download the required data from the ncbi ftp)
>>> /beegfs/data/id/myconda/bin/taxadb download -o taxadb

(If you work only on protein sequences, no need to download the all db (-d prot option only get protein informations)
>>> nohup /beegfs/data/id/myconda/bin/taxadb create -i /beegfs/data/id/taxadb --dbname taxadb.sqlite -d prot --fast &> nohup.out&

#The taxadb.sqlite file will by created in the direcotry where is run the command. 

"""

"""
Input exemple file:
query	target	pident	alnlen	qstart	qend	tstart	tend	evalue	bits
scaffold_1	ACT53096.1	33.3	102	1	295	158	259	1.19e-12	64
scaffold_2	ADR03158.1	28.9	183	3	531	98	271	2.516e-16	78
scaffold_3	BAV91453.1	26.1	168	9	486	63	227	2.294e-07	51

Output exemple file: 
	query	target	pident	alnlen	qstart	qend	tstart	tend	evalue	bits	Taxid	species	genus	subfamily	family	superfamily	parvorder	infraorder	suborder	order	superorder	no rank	class	superclass	subphylum	phylum	kingdom	superkingdom	subgenus	subcohort	cohort	infraclass	subclass
0	scaffold_1	ACT53096.1	33.3	102	1	295	158	259	1.19e-12	64	9606	Homo sapiens	Homo	Homininae	Hominidae	Hominoidea	Catarrh
ini	Simiiformes	Haplorrhini	Primates	Euarchontoglires	cellular organisms	Mammalia	Sarcopterygii	Craniata	Chordata	Metazoa	Eukaryota		
1	scaffold_2	ADR03158.1	28.9	183	3	531	98	271	2.516e-16	78	10090	Mus musculus	Mus	Murinae	Muridae				Myomorpha	Rodentia	Euarchontoglires	cellular organisms	Mammalia	Sarcopterygii	Craniata	Chordata	Metazoa	Eukaryota	Mus				
2	scaffold_3	BAV91453.1	26.1	168	9	486	63	227	2.294e-07	51	487618	Danio margaritatus	Danio		Cyprinidae				Cyprinoidei	Cypriniformes	Cypriniphysae	cellular organisms	Actinopteri	Actinopterygii	Craniata	Chordata	Metazoa	Eukaryota		Ostariophysi	Otomorpha	Teleostei	Neopterygii

"""

#In order to get the processing time
start_time = time.time()

# Variable that stores the options given by the user
blast_file=args.blast
out_file=args.out
taxadb_sqlite_file=args.taxadb_sqlite_file
#blast_file="/beegfs/home/bguinet/M2_script/dataframe_brute.txt"
#taxadb_sqlite_file="/beegfs/data/bguinet/taxadb.sqlite"
out_file="/beegfs/home/bguinet/M2_script/Out_file.m8"


accession = AccessionID(dbtype='sqlite', dbname=taxadb_sqlite_file)
taxid = TaxID(dbtype='sqlite', dbname=taxadb_sqlite_file)
blast=pd.read_csv(blast_file,header=0,sep="\t")

#Create a dataframe to store the Acc_number and Taxid
blast_taxid=pd.DataFrame(columns=['Acc_number','Taxid']) 

liste=[]
for i in blast.target.str.split(".").str[0]:    #<--------- change "target" to the colname of the Acc_number (ssid in blast and diamond; target in mmseqs2)
	liste.append(i)

#Remove duplicate acc_number
liste = list(dict.fromkeys(liste))

# Function to return smaller lists of the larger list.
def chunk(items,n):
    for i in range(0,len(items),n):
        yield items[i:i+n]

n=round(len(liste)/990)+1


def Get_taxid_inf(blast_file):
	accession = AccessionID(dbtype='sqlite', dbname=taxadb_sqlite_file)
	taxid = TaxID(dbtype='sqlite', dbname=taxadb_sqlite_file)
	blast=pd.read_csv(blast_file,header=0,sep="\t")

	#Create a dataframe to store the Acc_number and Taxid
	blast_taxid=pd.DataFrame(columns=['Acc_number','Taxid']) 

	liste=[]
	for i in blast.target.str.split(".").str[0]:    #<--------- change "target" to the colname of the Acc_number (ssid in blast and diamond; target in mmseqs2)
		liste.append(i)

	#Remove duplicate acc_number
	liste = list(dict.fromkeys(liste))
	# Break the larger list into length 10 lists.
	count_row = len(liste)
	filecount = 1
	for subitems in chunk(liste,n):
		taxids = accession.taxid(subitems)
		for tax in taxids:
			blast_taxid.loc[len(blast_taxid)]=[tax[0],tax[1]]

			filled_len = int(round(50 * filecount / float(count_row -1)))
			percents = round(100.0 * filecount / float(count_row ), 1)
			bar = '=' * filled_len + '-' * ((50) - filled_len)
			sys.stdout.write('[%s] %s%s Get Tax Id...%s\r' % (bar, percents, '%', ''))
			sys.stdout.flush()  # As suggested by Rom Ruben
			filecount += 1


	blast['Taxid']=blast.target.str.split(".").str[0].map(dict(zip(blast_taxid.Acc_number,blast_taxid.Taxid)))

	print("\n")

	d = {}

	count_row = blast_taxid.shape[0]
	filecount = 1
	taxid = TaxID(dbtype='sqlite', dbname=taxadb_sqlite_file)
	for i in blast_taxid['Taxid']:
		d[i] = taxid.lineage_name(i, ranks=True,reverse=True)
		filled_len = int(round(50 * filecount / float(count_row -1)))
		percents = round(100.0 * filecount / float(count_row ), 1)
		bar = '=' * filled_len + '-' * ((50) - filled_len)
		sys.stdout.write('[%s] %s%s Get lineage information...%s\r' % (bar, percents, '%', ''))
		sys.stdout.flush()  # As suggested by Roid', right_index=True)
		filecount += 1

	blast=blast.merge(pd.DataFrame.from_dict(d, orient='index'), left_on='Taxid', right_index=True,)
	blast.fillna('NA', inplace=True)
	#Remove all spaces en replace them by _ - double check
	blast.columns = blast.columns.str.replace(' ', '_')
	blast=blast.replace(' ', '_', regex=True)


	blast.to_csv(out_file, sep='\t')

Get_taxid_inf(blast_file)

print("\n")
print("Process done")
print("Output written at: ",out_file)
print("--- %s seconds ---" % (time.time() - start_time))

