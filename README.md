# Gruppe 06

## Mitglieder

- Alex Hergett
- Clara Leidhold
- Georg Schneeberger

## General info

We have 3 important scripts.
- generate_dataset.py
- recognition_pipeline.py
- analyse_results.py

We use YML files to configure the first 2 scripts.
- example_dataset_generate_config.yaml is the default config used by generate_dataset.py
- example_recognition_config.yaml is the default config used by recognition_pipeline.py

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
conda install -n acg pyyaml

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


