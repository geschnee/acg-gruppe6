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


# how to use
- Install Erdbeermet package 
- Install requirements.txt
- generate Dataset
  - in example_dataset_generate_config.yaml under config_sets adjust
    1. foldername ("set_name:")
    2. number of generated nodes ("n:")
    3. circularity or non-circularity
    4. clockwise or non clockwise
    5. amount of files generated for one config ("size:")
  - either for each configuration or as default parameters
  - run generate_dataset.py


- choose algorithm for recognition
  - in example_recognition_config.yaml:
    1. base for original algorithm
    2. spike for modified for spike lengths
    3. reserve-3 for first 3 nodes fixed correctly
    4. reserve-4 for first 4 nodes fixed correctly
    5. realistic-3 for first 3 nodes fixed randomly
    6. realistic-4 for first 4 nodes fixed randomly
    - plus adjust dataset path and result folder


- run recognition_pipeline.py

- to get result-plots:
  - run analyse_results.py

