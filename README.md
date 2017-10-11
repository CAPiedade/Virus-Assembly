# Virus Disassembly

Python2.7 Code designed to calculate the interactions of a *T=1* Virus Capsid based on the group symmetry of the arrangement of the proteins.

This code allows to generate the different combinations of removing *N* proteins of a capsid based on the Icosahedral Group Symmetry.


#### Use

Run the code in the folder where your PDB file is.

The PDB file must have each chain in a different model for it to work.

#### Dependencies

+ Numpy
+ BioPython
+ Anaconda Python is reccomended for other modules
+ igraph

(anyothers that you may find, please inform me to add)

#### WARNING

This code will generate large amounts of data!

Don't forget to check which Heuristic measure you are using by changing the Energy Points in File EnergyCalc_fun.py

#### How to Use

+ Run the programs in this order (making the proper modifications to the programs to adapt to your situation)
  + downloadpdbT1tofolder.py
  + Calcular.py
  + EnergyCalc2.py
    + Be sure to have the files GraphSymmetries___.txt and EnergyCalc_fun.py in the same folder and EnergyCalc2.py)
    + Change the Energy Points in EnergyCalc_fun.py to your desired heuristic
  + Tree_Graph.py
    + Program with #exit() commands strategically positioned to select render best performance
  + Analize the files graph_path_dEdN.txt for each PDB and look for the lowest energy combination

  

+ When needed, use the files in the folders Group Symmetries and Graph Symmetries or generate them by running
  + gen_subgroups_recursive.py (you'll always need an origin file from where to start the recursion, such as the one provided in Group Symmetries)
  + gen_subgroups.py (create the subgroups from scratch)
  + graph.py (for Graph Symmetries based on the Group Symmetries you have)

#### Problems Still to Solve

+ If some aminoacids are incomplete
+ T-number bigger than 1
+ Faster algorithm to build the Tree Graph of pathways


#### Author

Cláudio Alexandre Guerra Silva Gomes da Piedade

PhD Student of Applied Mathematics at Faculdade de Ciências da Universidade do Porto (Oporto, Portugal)

MSc in Biochemistry (2016)
