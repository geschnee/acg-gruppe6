from itertools import permutations
import sys
import yaml
import glob
import erdbeermet.simulation as sim
import erdbeermet.recognition as rec
import recognition_algorithms.modified_recognition as modrec
import recognition_algorithms.WP4_modified_recognition as wp4rec
import os
import time
import copy
import random
from enum import Enum
import shutil


def readConfigFile(configfile):
    with open(configfile, "r") as stream:
        dict = {}
        try:
            dict = yaml.safe_load(stream)
            return dict
        except yaml.YAMLError as exc:
            print(exc)


def getFilesToAnalyse(foldername, dataset_location):
    files = glob.glob(os.path.join(dataset_location, foldername) + '/*.txt')
    # finds all .txt files in foldername
    # the folder should only contain .txt files that are history files generated by simulation

    return files


def getSimulationParams(foldername):
    sim_n = "unknown"
    sim_circular = "unknown"
    sim_clockwise = "unknown"

    for s in foldername.split("_"):
        if s == "small":
            sim_n = 6
        if s == "medium":
            sim_n = 7
        if s == "big":
            sim_n = 8
        if s == "circular":
            sim_circular = True
        if s == "noncircular":
            sim_circular = False
        if s == "clockwise":
            sim_clockwise = True
        if s == "nonclockwise":
            sim_clockwise = False

    return sim_n, sim_circular, sim_clockwise


def readScenario(h_file):
    return sim.load(h_file)


def isDirectory(dir):
    return os.path.isdir(dir)


def createDir(dir):
    if not isDirectory(dir):
        os.makedirs(dir)


def recognitionSuccessful(r_tree):
    for v in r_tree.preorder():  # v are vertices in the recognition tree
        if v.valid_ways > 0:
            # a successful recognition path was found -> recognition was successful
            # the intuition behind this validation come from write_recognition in FileIO.py (erdbeermet)

            # if there is at least one path with a valid recognition, then we recognised it successfully
            # but of course not necessarily identical to the corresponding simulation r-steps
            return True
    return False


def succesfulRecognitions(r_tree):
    # how many green paths are there in the tree
    return len(getValidRStepSequences(r_tree))


def traverseTree(node, sequence, paths):
    if node.valid_ways == 0:
        # no valid path in the child nodes of this node, thus no valid paths can be built from this node
        # we can therefore return here and not analyse more
        return

    cloned_sequence = copy.deepcopy(sequence)

    cloned_sequence.append(node)
    # append the node to the sequence/path

    if not node.children:  # node has no children --> is a leaf node
        # add node to sequence and add sequence to paths
        # since we are at a child node we can return
        paths.append(cloned_sequence)
        return

    for child in node.children:
        traverseTree(child, cloned_sequence, paths)


def traversalToRstepSequences(forwardPath):
    # transforms a traversal of the recognition tree (root to leaf)
    # into a sequence of r-steps ("going" from leaf to root of recognition tree)

    forwardPath.reverse()  # reverse initial order (initial order is from root to leaf)

    sequence = []

    counter = 4  # leaf node has 4 elements, moving up the tree 1 node is added each step
    for step in forwardPath:
        assert len(step.V) == counter
        # step.V is the list of graph-nodes at that recognition_tree-node
        # here we got a simple check to see if the list increases
        # if it does not, there is some kind of bug we need to find

        counter += 1
        sequence.append({"V": step.V, "r-step": step.R_step, "D": step.D})

    return sequence


def getValidRStepSequences(recognition_tree):
    # returns the sequences of valid r-steps

    paths = []

    # traversing a recognition tree from the root to the child nodes shows the reverse r-steps used to construct the tree
    # thus we traverse from root to child and then revert the steps to get the validRStepSequences
    # when traversing from root to children we can check the attribute valid_ways on each node
    # if valid_ways==0 we can abort the processing of that node and discard the path up to this node
    # if we reach a leaf node and the node has valid_ways == 1, we found a good path, that we can build the sequence of r-steps and add to the paths list

    traverseTree(recognition_tree.root, [], paths)
    # paths object now contains the paths of r-steps, going from root to leaf
    # traverseTree is a recursive function
    # paths are not reversed here

    for path in paths:
        assert len(path) == recognition_tree.root.n - 3
        # len(path)==depth_of_tree==n-4+1
        # -4+1 since the starting point contains 4 nodes
        # n=root_node.n
        # recognition_tree == root

    # paths contains lists of nodes, we need to do more processing here
    r_step_sequences = []
    for path in paths:
        r_step_sequences.append(traversalToRstepSequences(path))

    return r_step_sequences


def xLeafMapMatchesSimulation(reconstructed_r_step_sequence, x=4):
    # Purpose of this method:
    # ??? Classify whether the final 4-leaf map after recognition matches the first 4 leaves of the simulation.

    # Explain Datatypes
    # reconstructed_r_step_sequence is a green path of the erdbeermet recognition
    # reconstructed_r_step_sequence[0] is the leaf node of a recognition_tree
    # leaf_node_of_path
    # reconstructed_r_step_sequences[0] contains a list of 4 nodes
    # the 4 nodes are the final x-leaf map after recognition

    leaf_node_of_path = reconstructed_r_step_sequence[0]
    recognition_leafs = leaf_node_of_path["V"]

    # abuse the ordering
    # the first x nodes, that are added during simulation, are range(x)
    for i in range(x):
        if not i in recognition_leafs:
            return False

    # ask how should we compare these?
    # just check if the first x nodes of simulation_r_step_sequences are in reconstructed_r_step_sequence[0]?
    # yes, that is correct
    # this would not check the ordering
    # probably this because we stop at 4 leaves and assume their ordering does not matter

    return True


def buildSimulationSequence(original_scenario):
    r_step_sequence = []
    for x, y, z, alpha, delta in original_scenario.history:
        # from erdbeermet simulation.py print_history

        # sort parents of triples
        if x <= y:
            r_step_dict = {
                "x": x,
                "y": y,
                "z": z
            }
        else:
            r_step_dict = {
                "x": y,
                "y": x,
                "z": z
            }
        r_step_sequence.append(r_step_dict)

    return r_step_sequence


def number_cooptimal_sol(all_green_paths):
    # cooptimal solutions are paths were the node order is different from the simulation ones
    paths_out_of_order_count = 0
    for path in all_green_paths:
        normal_seq = [[0, 1, 2, 3]]
        for index in range(1, len(path)):
            save = copy.deepcopy(normal_seq[index - 1])
            save.append(index + 3)
            normal_seq.append(save)
        node_order = []
        for step in path:
            node_order.append(step["V"])
        if not normal_seq == node_order:
            paths_out_of_order_count += 1
    return paths_out_of_order_count


def commonTriples(reconstruction_sequence, simulation_sequence):
    # ask professors
    # what about the starting point of reconstruction???? (it is a list of 4 nodes)
    # do we always consider them as being common triples? (3 triples)
    # only when they are the nodes 0, 1, 2, 3 ?
    # asked this on Thursday
    # we do not have to check this
    # given a simulation with 6 nodes
    # the maximum number of common tripes is 2 (6-4)

    # basically common triples only checks the r-steps in the recognition path, nodes in recognition leaf are not considered

    # a triple is x, y, z
    # x and y are the "parents"
    # z is their child

    # we do not check the alpha, is that okay?
    # Professors confirmed on 05.01. that we do not need to check the alpha
    # They basically assume the alpha is always correct (between two common triples).

    recognition_r_steps = set()  # set of r-steps
    for r in reconstruction_sequence:
        if r["r-step"]:  # has an r-step
            r_step = r["r-step"]

            # the next line was included in our original cobe
            # I just noticed this is a bug. However this bug will not have had any impact.
            # The returned simulation_r_steps.intersection(recognition_r_steps) is not affected.
            # recognition_r_steps.add(f'({r_step[0]}, {r_step[1]}: {r_step[2]})')  # represent r-step as string like in history file
            # This added not needed entries to recognition_r_steps


            # bring parents in numerical order
            if r_step[0] <= r_step[1]:
                recognition_r_steps.add(
                    f'({r_step[0]}, {r_step[1]}: {r_step[2]})')  # represent r-step as string like in history file
            else:
                recognition_r_steps.add(
                    f'({r_step[1]}, {r_step[0]}: {r_step[2]})')
    simulation_r_steps = set()  # set of r-steps
    for s in simulation_sequence:
        # represent r-step as string like in history file
        simulation_r_steps.add(f'({s["x"]}, {s["y"]}: {s["z"]})')

    # recognition_r_steps contains the triples from the recognition path
    # simulation_r_steps contains the triples from the simulation
    return simulation_r_steps.intersection(recognition_r_steps)


def choosePathRandomly(paths):
    # From Praktikumsbeschreibung:
    # Out of the list of candidates for the last step choose a random, positive one if it exists. Use this option also for WP3 and WP4

    if len(paths) < 1:
        return False

    index = random.randrange(len(paths))  # generate a random index

    return paths[index]


def realistic_recognition(D, B_set_size):
    # Assume the realistic case where the core leaves are not known. Write a wrapper that iterates through all subsets of 4 or respectively 3 leaves until an R-map was correctly identified. Benchmark as in WP2.

    B_sets = list(permutations(range(len(D)), B_set_size))

    random.shuffle(B_sets)
    # we need to shuffle the permutations, else the first element in B_sets would always be [0, 1, 2] or [0, 1, 2, 3] depending on B_set_size

    for B_set in B_sets:
        tree = modrec.modified_recognize(D, B_set, first_candidate_only=True)

        # tree.visualize()
        if recognitionSuccessful(tree):
            # until an R-map was correctly identified
            # early stopping
            return tree

    # recognition was not succesful for any of the combinations
    # to prevent any bugs with our dirty code, we should give a failed recognition tree back

    # return the tree built from the last permutation
    return modrec.modified_recognize(D, B_sets[-1], first_candidate_only=True)


def reserved(D, reserved_size):
    B_set = list(range(reserved_size))
    return modrec.modified_recognize(D, B_set, first_candidate_only=True)


def base_alg(D):
    return rec.recognize(D, first_candidate_only=True)


def base_spike(D):
    return wp4rec.spike_recognize(D, first_candidate_only=True)


def get_recognition_tree(algo, d_matrix):
    recognition_tree = None
    if algo == 'base':
        recognition_tree = base_alg(d_matrix)
    elif algo == 'reserve-3':
        recognition_tree = reserved(d_matrix, 3)
    elif algo == 'reserve-4':
        recognition_tree = reserved(d_matrix, 4)
    elif algo == 'realistic-3':
        recognition_tree = realistic_recognition(d_matrix, B_set_size=3)
    elif algo == 'realistic-4':
        recognition_tree = realistic_recognition(d_matrix, B_set_size=4)
    elif algo == 'spike':
        recognition_tree = base_spike(d_matrix)

    return recognition_tree


def backupFailedHistory(h_file, config, algo):

    createDir(os.path.join(config["result_folder"],
              "failed_recognitions", algo))

    cleaned_filename = h_file.replace('\\', '/')
    cleaned_filename = cleaned_filename.split("/")[-1]

    # copy h_file to the appropriate folder
    shutil.copy(h_file, os.path.join(
        config["result_folder"], "failed_recognitions", algo, cleaned_filename))


def recognizeFile(h_file, config, algo):
    # this method analyses a single file from a dataset

    print(f'\n\n\n')
    print(f'======================================')
    print(f'Start analysis of {h_file} with {algo}')

    result_object = {}
    original_scenario = readScenario(h_file)

    simulation_sequence = buildSimulationSequence(original_scenario)

    # get distance matrix ("real" input for recognition) from history (Erdbeermet)
    d_matrix = original_scenario.D

    #########################################
    ## Recognition with the correct algorithm
    #########################################

    ts_before = time.time()
    recognition_tree = get_recognition_tree(algo, d_matrix)
    ts_after = time.time()
    duration = ts_after - ts_before
    result_object["duration"] = duration


    ###############################################
    ## Analysis of the constructed recognition tree
    ###############################################

    print(f'ts_before {ts_before}')
    print(f'ts_after {ts_after}')
    print(f'Duration {duration}')

    print(f'Recognition successful {recognitionSuccessful(recognition_tree)}')
    print(
        f'Recognition successful total {succesfulRecognitions(recognition_tree)}')

    # getValidRStepSequences returns all the green paths
    all_green_paths = getValidRStepSequences(recognition_tree)

    path = choosePathRandomly(all_green_paths)

    anzahl_matched_leaves = 0
    for i in all_green_paths:
        if xLeafMapMatchesSimulation(i):
            anzahl_matched_leaves += 1

    if recognitionSuccessful(recognition_tree):

        random_path_matched = 0
        if xLeafMapMatchesSimulation(path):
            random_path_matched = 1
        result_object["4_Leaves_matches_simulation_count"] = random_path_matched

        result_object["Recognition successful total"] = succesfulRecognitions(
            recognition_tree)
        # Classify whether the final 4-leaf map after recognition matches the first 4 leaves of the simulation.
        print(f'4 leaf matches {xLeafMapMatchesSimulation(path, 4)}')
        result_object["final_three_matches_simulation"] = xLeafMapMatchesSimulation(
            path, 3)
        result_object["final_four_matches_simulation"] = xLeafMapMatchesSimulation(
            path, 4)

        result_object["Percentage of 4 Leaves map matches simulation"] = (
            anzahl_matched_leaves/len(all_green_paths))*100

        # Measure divergence of the reconstructed steps from true steps of the simulation, e.g. by counting common triples.
        print(f'common triples {commonTriples(path, simulation_sequence)}')
        result_object["common_triples"] = commonTriples(
            path, simulation_sequence)
        result_object["number_of_common_triples"] = len(
            commonTriples(path, simulation_sequence))
        try:
            result_object["percent_of_common_triples"] = len(commonTriples(path, simulation_sequence)) / (
                len(path) - 1) * 100
            print(
                f'percentage_of_common_triples {result_object["percent_of_common_triples"]}')
        except ZeroDivisionError:
            result_object["percent_of_common_triples"] = 0
    else:
        # do the processing when no valid path was found

        result_object["final_three_matches_simulation"] = False
        result_object["final_four_matches_simulation"] = False
        result_object["common_triples"] = "no common triples"
        result_object["number_of_common_triples"] = 0
        result_object["percent_of_common_triples"] = 0
        result_object["Recognition successful total"] = 0

        result_object["4_Leaves_matches_simulation_count"] = 0

        # no green path does 0 percentage 4 leave map matches -> always 0
        result_object["Percentage of 4 Leaves map matches simulation"] = 0

        # save the history file of the failed recognition
        backupFailedHistory(h_file, config, algo)

    # co optimal solutions
    result_object["co_optimal_solutions"] = number_cooptimal_sol(
        all_green_paths)
    print(f'co_optimal_solutions {result_object["co_optimal_solutions"]}')

    result_object["recognition_success"] = recognitionSuccessful(
        recognition_tree)
    # Classify whether the distance matrix was correctly recognized as an R-Map.
    # is True when there was at least one green path
    result_object["recognition_success_total"] = succesfulRecognitions(
        recognition_tree)
    # Amount of green paths in recognition tree

    return result_object


def getDirectoriesToAnalyse(datasets_directory):
    folders = [name for name in os.listdir(datasets_directory) if os.path.isdir(
        os.path.join(datasets_directory, name))]
    # finds all directories in datasets_directory
    return folders


def setupDirectoryForFailedRecognitions(config):
    createDir(os.path.join(config["result_folder"], "failed_recognitions"))

    for a in config["recognition_algorithms"]:
        createDir(os.path.join(config["result_folder"], "failed_recognitions", a))


def analyse(configfile):
    # this method tries the recognition of the folders in config["dataset_folder"]
    # for each algorithm in config["recognition_algorithms"]

    # read config yaml file, return python dictionary (config)
    config = readConfigFile(configfile)
    createDir(config["result_folder"])

    setupDirectoryForFailedRecognitions(config)

    folders = getDirectoriesToAnalyse(config["dataset_folder"])

    for f in folders:
        for algorithm in config["recognition_algorithms"]:
            analyseFolder(f, config, algorithm)


def countFailures(results):
    failure_count = 0

    for r in results:
        if r["recognition_success"] == False:
            failure_count += 1

    percentage = failure_count/len(results) * 100
    return failure_count, percentage


def analyseFolder(folder, config, algo):
    # analyses a folder like this one:
    # datasets/example_dataset/circular
    
    history_files = getFilesToAnalyse(folder, config["dataset_folder"])
    sim_n, sim_circular, sim_clockwise = getSimulationParams(folder)

    count_path = {}

    createDir(config["result_folder"])
    #createDir(os.path.join(config["result_folder"], folder))

    results = []
    # results list contains the results of the individual anlysis

    common_triples_count = 0
    common_triples_percentage = 0
    total_duration = 0
    four_leaf_matches_simulation_test = 0
    correctly_classified_r_maps = 0
    correctly_classified_r_map = 0
    number_of_co_optimal_solutions = 0
    percentage_four_leaf_matches_simulation = 0
    for h in history_files:
        result_object = recognizeFile(h, config, algo)
        h_rmap = 1 if result_object["recognition_success"] is True else 0
        correctly_classified_r_map = correctly_classified_r_map + h_rmap
        common_triples_count = common_triples_count + \
            result_object["number_of_common_triples"]
        common_triples_percentage = (
            common_triples_percentage + result_object["percent_of_common_triples"])
        if result_object["Recognition successful total"] in count_path.keys():
            count_path[result_object["Recognition successful total"]
                       ] = count_path[result_object["Recognition successful total"]] + 1
        else:
            count_path[result_object["Recognition successful total"]] = 1
        four_leaf_matches_simulation_test = four_leaf_matches_simulation_test + \
            result_object["4_Leaves_matches_simulation_count"]
        percentage_four_leaf_matches_simulation = percentage_four_leaf_matches_simulation + \
            result_object["Percentage of 4 Leaves map matches simulation"]
        correctly_classified_r_maps = correctly_classified_r_maps + \
            result_object["recognition_success_total"]
        number_of_co_optimal_solutions = number_of_co_optimal_solutions + \
            result_object["co_optimal_solutions"]
        total_duration = total_duration + result_object['duration']

        # the results of recognizeFile() are a python dictionary
        results.append(result_object)

    common_triples_count = common_triples_count / len(history_files)
    common_triples_percentage = common_triples_percentage / len(history_files)
    print(f'average number of common triples: {common_triples_count}')
    print(
        f'average percentage of common triples: {common_triples_percentage} %')

    avarage_duration = total_duration / len(results)
    print(f'1 result object {results[0]}')
    print(f'avarage duration {avarage_duration}s')

    # results now contains the result_object of the individual files
    # result_object is generated by recognizeFile()

    _, failuresPercentage = countFailures(results)

    d = {
        "Algorithm": algo,
        "Simulation N": sim_n,
        "Simulation circular": sim_circular,
        "Simulation clockwise": sim_clockwise,
        "Files analysed": len(history_files),
        "Total time elapsed": total_duration,
        "Average duration time": avarage_duration,
        "Percentage of common triples": str(common_triples_percentage) + "%",
        "Count path distribution": count_path,
        "Percentage of 4-Leaf Maps Matching Simulation": str(percentage_four_leaf_matches_simulation/len(history_files)) + " %",
        "Average of random 4-Leaf Maps Matching the Simulation": four_leaf_matches_simulation_test/len(history_files),
        "Percentage of failed recognitions": str(failuresPercentage) + "%",
        "Percentage of correctly classified R-Maps": str((correctly_classified_r_map / len(history_files)) * 100) + " %",
        "Average Number of co-optimal solutions": number_of_co_optimal_solutions / len(history_files),
    }

    # dictionary zum abspeichern,
    createDir(os.path.join(config["result_folder"], 'recognition_summaries'))
    yaml_name = os.path.join(config["result_folder"], 'recognition_summaries',
                             f'{folder}_{algo}_result.yml')

    with open(yaml_name, 'w') as yaml_file:
        yaml.dump(d, yaml_file, default_flow_style=False)


if __name__ == '__main__':
    recognition_config = "example_recognition_config.yaml" if len(
        sys.argv) == 1 else sys.argv[1]
    print(f'Analysis Files: {recognition_config}')

    ts_before = time.time()
    analyse(recognition_config)
    ts_after = time.time()

    print(f'Total duration {ts_after - ts_before}')
