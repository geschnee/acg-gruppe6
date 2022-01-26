# graphen-verstehen
Repo zum Seminar/Praktikum


# Grober Plan

## WP 1

* the distance matrix should be provided to the recognition algorithm in the form of history files
    * from this history file the standard recognition can reconstruct the distance matrix
        * erdbeermet.simulation.load(filename).distances()
    * our recognition algorithm can then use that distance matrix
    * the first 4 leaves of the simulation can also be read from the history file
        > Classify whether the final 4-leaf map after recognition matches the first 4 leaves of the simulation
        > Write a wrapper function that passes the first 4 or respectively 3 leaves of the simulation as B and benchmarks results as in WP2.
* several configs are needed
    * how about example_config.yaml ?
    * we can pass this to the recognition pipeline as input
        * this makes the parameters more readable and the executions more reproducible


# WP1: Simulation

What are these parameters?
## Circular
> If set to True, the resulting distance matrix is guaranteed to be a circular type R matrix. The default is False.

TODO Would that mean the resulting distance matrix could always be used to reconstruct the r-step history?

## Clockwise
> If set to True, the distance increment is equal for all items within each iteration (comprising a merge or branching event and the distance increments) and only varies between iteration. The default is False, in which case the increments are also drawn independently for the items within an iteration.

## Common Triples
- given a path in a recognition tree and a simulation sequence gives intersection of common triples
- in recognizeFile (recognition of h_file): choosing one path out of rec tree randomly - for this one do: 
result_object[\'percent_of_c_t\'] = len(commonTriples(path, sim_sequence)) / (len(path) - 1) * 100))
- len(path) - 1 because path includes empty element for stopping
- in analyseFolder:
common_triples_percentage = sum of result_object[\'percent_o_c_t\'] of every h-file
- Final metric: Average common_triples_percentage on sum of history files

##Number of Co-optimal Solutions
- in number_cooptimal_sol(array of paths): returns number of paths, which dont have ideal order
- In recognizeFile:compute number of co-optimal solutions of all green paths of tree
- result_object(number of cooptimal solutions) gives number of green paths in tree which arent ideal (absolute number)
- In analyseFolder: number of co-optimal solutions are averaged over all history files

## Percentage of failed recognitions
- failed recognition == recognition tree has no green paths
- percentage is computed over all the history files

# Notiz

for every combination of ....
20.000 bedeutet 20.000 Datasets (history files)
 
6+ leaves verwenden


Measure the divergence of the reconstructed steps....

WP2
choose a random positive one if it exists
(das bezieht sich auch auf das classify whether the final 4 leaf map is correct)


Ergaenzung zu common triplets:
die alphas muessen wir nicht checken.
(die Annahme der Professoren ist, dass es nicht vorkommen kann, dass ein falsches alpha in der Recognition entsteht)
da wir uns nicht um die Alphas kuemmern, muessen wir auch nicht die Reihenfolge der Parents beachten.

Ein Check des Alphas waere eine gute Extraleistung, laut Professoren.


Freitag 14 Uhr nochmal


# Run on server

## copy repo to server
scp -r graphen-verstehen/ gpraktikum06@k60.bioinf.uni-leipzig.de:/scratchsan/praktikum/gpraktikum06/repo/


## connect to server

ssh gpraktikum06@k60.bioinf.uni-leipzig.de

## get Erdbeermet

- git clone https://github.com/david-schaller/Erdbeermet
- cd Erdbeermet
- conda create --name bla python=3.9
- conda activate bla
- python setup.py install

## prepare repo

cd repo
conda install -n bla pyyaml

## now the repo is ready to be used

## run a python script in background

we need to be able to run the script in the background (so we can disconnect and the script continues)

nohup python recognition-pipeline.py &


nohup causes the output to be placed in a nohup.out file
& causes the process to be running in the background

# Links
* [Erdbeermet Repo](https://github.com/david-schaller/Erdbeermet#generation-of-scenarios)
* [ACG-gruppe6](https://github.com/geschnee/acg-gruppe6)
* [Praktikumsdokumente](http://silo.bioinf.uni-leipzig.de/GTPraktikumRMaps/)
