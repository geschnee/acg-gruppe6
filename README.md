# Gruppe 06

## Mitglieder

- Alex Hergett
- Clara Leidhold
- Georg Schneeberger


# General info

We have 3 important scripts.
- generate_dataset.py
- recognition_pipeline.py
- analyse_results.py

We use YML files to configure the first 2 scripts.
- example_dataset_generate_config.yaml is the default config used by generate_dataset.py
- example_recognition_config.yaml is the default config used by recognition_pipeline.py

The config files can be changed or another one can be passed as a command line argument.

## Our Datasets

Unsere finale Analyse, welche auch in der Presentation verwendet wurde befindet sich im Ordner final_results. Eine Readme in diesem Ordner beschreibt auch die Datensets weiter.

# how to use

## Setup

- Install Erdbeermet package
- Install requirements.txt

## Generate Dataset
- generate Dataset
  - in example_dataset_generate_config.yaml under config_sets adjust
    1. foldername ("set_name:")
    2. number of generated nodes ("n:")
    3. circularity or non-circularity
    4. clockwise or non clockwise
    5. amount of files generated for one config ("size:")
  - either for each configuration or as default parameters
  - run generate_dataset.py

## Run Recognition
- choose algorithm(s) for recognition
  - in example_recognition_config.yaml:
    1. base for original algorithm
    2. spike for modified for spike lengths
    3. reserve-3 for first 3 nodes fixed correctly
    4. reserve-4 for first 4 nodes fixed correctly
    5. realistic-3 for first 3 nodes combination
    6. realistic-4 for first 4 nodes combination
    - plus adjust dataset path and result folder
- run recognition_pipeline.py

## Plot Results
- to get result-plots of folder final_results:
  - run analyse_results.py


# Our evaluation metrics

Our recognition_pipeline.py summarises the results in yml files.
Each of these yml files contains the results of one dataset (containing many simulation files generated with the same simulation parameters), analysed with one of our recognition algorithms. Dataset name and used algorithm are part of the yml file names, furthermore the exact details of simulation are also available in the yml files.

Generally our metrics like "Common Triples" and others treat a failed recognition as the worst case for that metric. Meaning a failed recognition contributes to the average percentage of common triples with a 0%.

## Percentage of correctly classified R-Maps / Percentage of failed recognitions
- Percentage of correctly classified R-Maps measures the percentage of succesful recognitions over all the files analysed in a dataset for an algorithm.
    - succesful recognition meaning the recognition returned a recognition tree with at leat 1 green path
- Percentage of failed recognitions is simply the inverse of Percentage of correctly classified R-Maps (100% - Percentage of correctly classified R-Maps)

## Average of random 4-Leaf Maps Matching the Simulation
- Percentage of the randomly chosen green recognition path's leaf matching the first 4 leaves of simulation.
- The percentage is computed over all recognitions of a dataset using one algorithm.

## Percentage of 4-Leaf Maps Matching Simulation
- Metric of 4-Leaf Maps Matching the Simulation, taking the average over all the green paths for one dataset and algorithm.

## Count path distribution

- Distribution of paths contains the counts of amounts of green paths after a recognition for one dataset and algorithm.
- Meaning if a recognition returned a tree with 3 green paths, the count for 3 is increased by one.
- A failed recognition increases the count for 0, since then there was no green path.


## Common Triples
- given a path in a recognition tree and a simulation sequence, Common Triples is the intersection of common triples of the r-steps
- the path of the recognition tree is chosen randomly (if multiple green ones exit)
- Final metric: Percentage of common triples
    * the average of the percentage

## Number of Co-optimal Solutions
- in number_cooptimal_sol(array of paths): returns number of paths, which dont have ideal order
- In recognizeFile: compute number of co-optimal solutions of all green paths of tree
- result_object(number of cooptimal solutions) gives number of green paths in tree which arent ideal (absolute number)
- In analyseFolder: number of co-optimal solutions are averaged over all history files
- Final metric: Average Number of co-optimal solutions
    * the average of the amount of non optimal green paths in the recognition tree


# Run on server

1. copy repo to server
    1. scp -r acg-gruppe06/ gpraktikum06@k60.bioinf.uni-leipzig.de:/scratchsan/praktikum/gpraktikum06/repo/
2. connect to server
    1. ssh gpraktikum06@k60.bioinf.uni-leipzig.de
3. get Erdbeermet
    * git clone https://github.com/david-schaller/Erdbeermet
    * cd Erdbeermet
    * conda create --name acg python=3.9
    * conda activate acg
    * python setup.py install
4. prepare repo
    * cd repo
    * conda install -n acg pyyaml
    * now the repo is ready to be used
5. run a python script in background
    * we need to be able to run the script in the background (so we can disconnect and the script continues)
    * nohup python recognition-pipeline.py &
    * nohup causes the output to be placed in a nohup.out file
    * & causes the process to be running in the background

# Links
* [Erdbeermet Repo](https://github.com/david-schaller/Erdbeermet#generation-of-scenarios)
* [ACG-gruppe6 Repo](https://github.com/geschnee/acg-gruppe6)
* [Praktikumsdokumente](http://silo.bioinf.uni-leipzig.de/GTPraktikumRMaps/)


