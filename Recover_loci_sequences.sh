#!/bin/bash
if [ $# -ne 3 ]
then
   echo "Please provide in the first argument the directory where are found all the Species directories"
   echo "Please provide in the second argument the directory where to found the file with all species names"
   echo "Please provide in the third argument the directory where to found the file Create_bed_file.py"
   echo "Example usage: bash Recover_loci_sequences.sh /beegfs/data/bguinet/M2/ /beegfs/home/bguinet/M2_script/ file_all_species_name.txt"
   exit 1
fi


cat $2$3 | while read line; do python3 $2Create_bed_file.py --table $1${line}/Matches_${line}_without_overlapping_sequences.m8 --out $1${line}/Recover_fasta_loci.bed; echo $'\n';
done 


cat $2$3 | while read line; do bedtools getfasta -fi $1${line}/${line}.fa -bed $1${line}/Recover_fasta_loci.bed -s -fo $1${line}/Fasta_viral_loci_seq_${line}.fa ; sed -i 's@)@):'${line}'@g' $1${line}/Fasta_viral_loci_seq_${line}.fa; echo "Loci sequences recovered and the output is written at : $1${line}/Fasta_viral_loci_seq_${line}.fa";
done
echo $'\n'

#Allows to get fasta sequences of viral loci with seq name such as :
#>scaffold_number:start-end(strand):Species_name

# -s Force strandedness. If the feature occupies the antisense strand, the sequence will be reverse complemented. Default: strand information is ignored.


#Now we will concatenate all viral loci sequences together 

echo $'Copying of files into a new file in order to contatenate them: \n'
cat $2$3 | while read line; do cp -v $1${line}/Fasta_viral_loci_seq_${line}.fa $1Viral_sequences_loci/Fasta_viral_loci_seq_${line}.fa; done
echo $'\n'

cat $1Viral_sequences_loci/Fasta_viral_loci_seq_* > $1Viral_sequences_loci/All_fasta_viral_loci.fna
echo "Concatenate succeed, ouput file written at : $1Viral_sequences_loci/All_fasta_viral_loci.fna"


#All_fasta_viral_loci.fna will contain all viral candidates loci
