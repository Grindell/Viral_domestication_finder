import pandas as pd
import numpy as np
from pandas import DataFrame
import os
import sys


num_species = sum(1 for line in open(sys.argv[1])) # count number of lines in the file in order to now the number of decimals / by the first number given
list_of_names1=[]
filecount = 1
for names in open(sys.argv[1],"r"):
	list_of_names1.append(names)

list_of_names2=[]

for names in list_of_names1:
	list_of_names2.append(names.replace("\n", ""))
df2 = pd.DataFrame(columns=('Total length', 'GC (%)', 'N50'))
for names in list_of_names2:
	df1=pd.read_csv("/beegfs/data/bguinet/these/Genomes/"+str(names)+"/Genome_assembly_statistics/transposed_report.tsv",sep="\t")
	cols = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,18,19,20,21]
	df1.drop(df1.columns[cols],axis=1,inplace=True)

	df2=df2.append({'Species_name':df1.iat[0,0],'Total length':df1.iat[0,1],'GC (%)':df1.iat[0,2],'N50':df1.iat[0,3]}, ignore_index=True)

	df2.to_csv('/beegfs/data/bguinet/these/Genomes/Assembly_summary.csv',sep='\t')

	filled_len = int(round(50 * filecount / float(num_species-1)))
	percents = round(100.0 * filecount / float(num_species), 1)
	bar = '=' * filled_len + '-' * ((50) - filled_len)

	sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', ''))
	sys.stdout.flush()  # As suggested by Rom Ruben


print(df2)
