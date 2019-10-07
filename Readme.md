#Work in progress, all the code will be uploaded in few weeks with a tutorial.


The developed pipeline involves the creation of certain files in well-established positions in the arborescence to ensure optimal fluidity
when executing scripts, then the results will be written at these paths.

First of all the user will have to make a file in which will be present all the genomes that he wants to study in format: Genus_species.fa
in the format : 

```
/Project/file_with_genomes: 
	Genus_speciesA.fa 
	Genus_speciesB.fa 
	Genus_speciesC.fa 
	Genus_speciesD.fa 
 ```
 
 Then, we will transforme it as: 
 
 ```
 /Project/Genus_speciesA
	Genus_speciesA.fa

/Project/Genus_speciesB
	Genus_speciesB.fa

/Project/Genus_speciesC
	Genus_speciesC.fa

/Project/Genus_speciesD
	Genus_speciesD.fa
 ```
 
 By creating a new directory having the same name as the ```Genus_species.fa``` file 
 
```
 DIR="/Users/admin/Documents/"

for file in $(find /Project/file_with_genomes -name "*.fa") 
do 
  name=$(basename "$file" .fa)
  mkdir -p $DIR/Project/$name 
  cp "$file" $DIR/Project/$name 
  echo $name >> $DIR/Project/file_all_species_name.txt 
done
```

This will creates: 
* A file called ```file_all_species_name.txt``` where in each line are written the species names.
* And each directory with ```the Genus_species name```. 


#Recherche de gènes BUSCO pour chacun des génomes. #
####################################################

Nous allons maintenant pour chacun des Génome, lui créer des fichiers Busco (run_busco) dans lesquels seront adressés tous les résultats des recherches BUSCO 


# Créer dans chacun des directory d'espèce une fichier run_busco qui contiendra les résultats du run avec BUSCO.V3 ainsi qu'un répertoire pour les logs
for dir in $DIR/Project/*; do mkdir -p $dir/run_busco/busco_job.log/; done

#2) Ensuite, créer des fichiers jobs Busco pour chacune de ces espèces et l'ajouter dans le fichier Busco_jobs
mkdir $DIR/Project/Scripts_pipeline/Busco_jobs


python3 Make_job_busco.py -i /beegfs/data/bguinet/these/Species_genome_names.txt  -o /beegfs/home/bguinet/these_scripts/Busco_jobs -p /beegfs/data/bguinet/these/

At the end of the process you should have the folowing message : 
----------------------------------------------------------------

                        Busco_job_maker.

----------------------------------------------------------------

[==================================================] 100.0% finish

132  files created at : /beegfs/home/bguinet/these_scripts/Busco_jobs


#3) Executer ensuite chacun de ces jobs 
for file in $DIR/Project/Busco_job*; do sbatch $file; done



#4) Pour chacun des fichiers de chaque espèce, rassembler les séquences protéiques et nucléiques ensembles
# 4.1) Créer un directory receveur pour les séquences prot et nucl
cat /beegfs/data/bguinet/these/Species_genome_names.txt | while read line; do  mkdir /beegfs/data/bguinet/these/Genomes/${line}/run_busco/run_${line}_BUSCO_v3/single_copy_busco_sequences/single_copy_busco_proteins; done
cat /beegfs/data/bguinet/these/Species_genome_names.txt | while read line; do  mkdir /beegfs/data/bguinet/these/Genomes/${line}/run_busco/run_${line}_BUSCO_v3/single_copy_busco_sequences/single_copy_busco_nucleotides; done

# 4.2) Déplacer toutes les séquences dans les bon fichiers correspondants 
cat /beegfs/data/bguinet/these/Species_genome_names.txt | while read line; do mv -v /beegfs/data/bguinet/these/Genomes/${line}/run_busco/run_${line}_BUSCO_v3/single_copy_busco_sequences/*.faa /beegfs/data/bguinet/these/Genomes/${line}/run_busco/run_${line}_BUSCO_v3/single_copy_busco_sequences/single_copy_busco_proteins/; done
cat /beegfs/data/bguinet/these/Species_genome_names.txt | while read line; do mv -v $DIR/Project/M2/${line}/run_busco/run_${line}_BUSCO_v3/single_copy_busco_sequences/*.fna /beegfs/data/bguinet/these/Genomes/${line}/run_busco/run_${line}_BUSCO_v3/single_copy_busco_sequences/single_copy_busco_nucleotides/; done

# Etape pour créer la base de donnée mmseqs2 et permet également d'alleger le nom des séquences busco (attention étape non complette dans la suite pour 5espèces)
cat /beegfs/data/bguinet/these/Species_genome_names.txt | while read line; do sed -i 's@:/beegfs/data/bguinet/these/Genomes/${line}/${line}.fa@@g' /beegfs/data/bguinet/these/Genomes/${line}/run_busco/run_BUSCO_v3/compiled_busco_aa

# 5) Récupérer un summary de tous les busco générés 
python3 /beegfs/home/bguinet/M2_script/Busco_summary.py /beegfs/home/bguinet/M2_script/file_all_species_name_and_outgroup.txt



