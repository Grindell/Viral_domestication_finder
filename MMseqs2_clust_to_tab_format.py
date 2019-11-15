import argparse
import networkx as nx
import pandas as pd
import sys 

# Print out a message when the program is initiated.
#print('-----------------------------------------------------------------------------------\n')
#print('                        ###Convert MMseqs2 clustering format to tabular#######.\n')
#print('-----------------------------------------------------------------------------------\n')

#----------------------------------- PARSE SOME ARGUMENTS ----------------------------------------
parser = argparse.ArgumentParser(description='Allow add taxonomy informationsa blast file')
parser.add_argument("-f", "--tsv_file", help="the blast file")
parser.add_argument("-o", "--out_dir", help="the output directory")
args = parser.parse_args()


#Allows to convert MMSeqs2 clustering tsv output into a tab format such as: 

#Cluster1 Seq1
#Cluster1 Seq2
#Cluster2 Seq3
#Cluster2 Seq4
#Cluster2 Seq5

#Where Seq1 and Seq2 are both in the same Cluster1 and Seq3,4 and Seq5 are in the Cluster2. 

MMseqs_tsv_file= args.btsv_file
Out_dir=args.out_dir


df = pd.read_csv(MMseqs_tsv_file, delimiter='\t',header=None)
df=df.rename(columns={0: "Col1", 1: "Col2"})
g = nx.from_pandas_edgelist(df, source='Col1', target='Col2', create_using=nx.Graph)

data = [[f'Cluster{i}', element] for i, component in enumerate(nx.connected_components(g), 1) for element in component]
result = pd.DataFrame(data=data, columns=['Cluster', 'Names'])

result.to_csv(Out_dir, sep='\t')

