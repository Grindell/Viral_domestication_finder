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


