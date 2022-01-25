from turtle import color
import yaml
import os
import numpy as np
import matplotlib.pyplot as plt
import math

colormap = {0: "red", 1: "limegreen", 2: "yellow", 3: "orange", 4: "orange", 5: "gold",
            6: "darkgoldenrod", 7: "saddlebrown", 8: "slategray", 9: "crimson"}


def readResults():
    results = list()
    directory = "final_results"  # os.path.join('results', 'benchmark')
    for file in os.listdir(directory):
        # TODO only if file ends with yml
        if not file.endswith(".yml"):
            continue

        with open(os.path.join(directory, file)) as yaml_file:
            try:
                data = yaml.safe_load(yaml_file)
                print(data)
                results.append(data)
            except yaml.YAMLError as exc:
                print(exc)

    return results


def filterN(results, n):
    filtered_results = list()

    for r in results:
        if r["Simulation N"] == n:
            filtered_results.append(r)

    return filtered_results


def filterCircular(results, circular):
    filtered_results = list()

    for r in results:
        if r["Simulation circular"] == circular:
            filtered_results.append(r)

    return filtered_results


def filterClockwise(results, clockwise):
    filtered_results = list()

    for r in results:
        if r["Simulation clockwise"] == clockwise:
            filtered_results.append(r)

    return filtered_results


def filterAlgorithm(results, algo):
    filtered_results = list()

    for r in results:
        if r["Algorithm"] == algo:
            filtered_results.append(r)

    return filtered_results


def readAlgorithms(results):
    algos = set()
    for r in results:
        # print(f'result {r}')
        # print(f'Algo {r["Algorithm"]}')

        algos.add(r["Algorithm"])

    # print(f'read algos {algos}')
    rtn = list(algos)
    rtn.sort()

    # print(f'rtn {rtn}')

    return rtn


def dictToDatasetName(dict):

    rtn = ""
    rtn = rtn+f'N={dict["Simulation N"]},\n'

    if dict["Simulation circular"]:
        rtn = rtn+f'Circular,\n'
    else:
        rtn = rtn+f'Noncircular,\n'

    if dict["Simulation clockwise"]:
        rtn = rtn+f'Clockwise'
    else:
        rtn = rtn+f'Nonclockwise'

    return rtn


def readDatasets(results):
    datasets = set()
    for r in results:
        # r["Algorithm"])
        datasets.add(dictToDatasetName(r))

    rtn = list(datasets)
    rtn.sort()

    return rtn


def percentagesByAlgorithm(results, algorithm, datasets):
    percentages = list()
    for i in datasets:
        for r in results:
            if dictToDatasetName(r) == i and r["Algorithm"] == algorithm:
                percentage_string = r["Percentage of correctly classified R-Maps"]
                percentage = float(percentage_string[:-1])
                percentages.append(percentage
                                   )
    return percentages


def getResult(raw_results, datasetname, algo):
    for r in raw_results:
        if dictToDatasetName(r) == datasetname and r["Algorithm"] == algo:
            return r
    return None


def buildColors(distribution):
    colors = list()
    for i in distribution.keys():
        colors.append(colormap[i])
    return colors


def countPathDistribution(raw_results):
    # one image per algorithm
    # image contains multiple pie charts
    # pie slices are the distributions

    algorithms = readAlgorithms(raw_results)

    for algo in algorithms:
        datasets = readDatasets(filterAlgorithm(raw_results, algo))

        # start new plot
        # for each dataset in datasets build piechart

        rows = math.ceil(len(datasets) / 4)
        coloumns = 4

        fig, ax = plt.subplots(rows, coloumns)
        fig.suptitle(
            f'Amount of Green paths for {algo} algorithm by dataset', fontsize=16, y=1)

        for index, d_name in enumerate(datasets):
            row = index % 4
            col = int(index / 4)

            dataset = getResult(raw_results, d_name, algo)
            distribution = dataset["Count path distribution"]

            labels = distribution.keys()
            sizes = distribution.values()

            mycolors = buildColors(distribution)

            s = 6

            if len(datasets) <= 4:
                ax[col].set_title(
                    d_name, size=s)
                ax[col].pie(sizes,
                            labels=labels, colors=mycolors, autopct='%1.1f%%',
                            shadow=False, startangle=90)
                # Equal aspect ratio ensures that pie is drawn as a circle.
                ax[col].axis('equal')
                # ax[col].tight_layout()

            else:
                ax[col, row].set_title(
                    d_name, size=s)
                ax[col, row].pie(sizes,
                                 labels=labels, colors=mycolors, autopct='%1.1f%%',
                                 shadow=False, startangle=90)
                # Equal aspect ratio ensures that pie is drawn as a circle.
                ax[col, row].axis('equal')
                #ax[col, row].tight_layout()

        for i in range(rows * coloumns - len(datasets)):
            i = i + len(datasets)

            row = i % 4
            col = int(i / 4)
            ax[col, row].axis('off')

        # plt.legend(["l1", "l2", "l3"], ["HHZ 1", "HHN", "HHE"])
        # colormap.keys(), colormap.values())

        plt.show()


def percentageCorrectlyClassified(raw_results):
    # grouped bar chart https://chartio.com/learn/charts/grouped-bar-chart-complete-guide/
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

    # y-axis is percentage
    # bars should be grouped by datasets
    # each bar should be one algorithm

    datasets = readDatasets(raw_results)

    algorithms = readAlgorithms(raw_results)

    percentages = {}

    print(f'Algorithms {algorithms}')
    for algo in algorithms:
        # percentages for algo for the different datasets
        algo_percentages = percentagesByAlgorithm(raw_results, algo, datasets)
        # ordering has to be the same as datasets
        percentages[algo] = algo_percentages

    x = np.arange(len(datasets))  # the label locations
    width = 0.1  # the width of the bars
    margin = 0.05

    fig, ax = plt.subplots()
    rects = list()
    for index, algo in enumerate(algorithms):
        ordering = index - int(len(algorithms) / 2)
        rects.append(ax.bar(x + ordering * (width + margin) + width / 2 + margin / 2,
                            percentages[algo], width, label=algo))

    # Add some text for datasets, title and custom x-axis tick datasets, etc.
    ax.set_ylabel('Succesful recognitions in %')
    ax.set_title('Succesful recognition by dataset and recognition Algorithm')
    ax.set_xticks(x, datasets)
    ax.legend(loc="lower right")

    for r in rects:
        ax.bar_label(r, fmt='%.0f', padding=3)

    fig.tight_layout()

    plt.show()


def failureSummary(raw_results):
    # build a table
    # coloumn headers are the datasets
    # row headers are the algorithms
    # fields are the number of failures

    totals = list()

    datasets = readDatasets(raw_results)

    algorithms = readAlgorithms(raw_results)

    for a in algorithms:
        row = list()
        sum = 0
        valid_entries = 0
        for d in datasets:
            dict = getResult(raw_results, d, a)
            if dict == None:
                row.append(-1)
            else:
                fail_percentage = float(
                    dict["Percentage of failed recognitions"][:-1])
                sum = sum + fail_percentage
                row.append(fail_percentage)
                valid_entries = valid_entries + 1

        print(f'row {row}')
        row.append(sum / valid_entries)
        # append the average

        totals.append(row)

    # build average for datasets
    dataset_average = list()
    for index, d in enumerate(datasets):
        sum = 0
        valid_entries = 0  # count the executed algorithms for the datasets
        for row in totals:
            if row[index] > -1:
                sum = sum + row[index]
                valid_entries = valid_entries + 1
        dataset_average.append(sum / valid_entries)
    # value for the average x average cell 9bottom right)
    dataset_average.append(-1)
    totals.append(dataset_average)

    print(f'totals {totals}')

    columns = datasets + ["average"]
    rows = algorithms + ["average"]

    # Get some pastel shades for the colors
    n_rows = len(rows)

    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(n_rows):
        r = list()
        for x in totals[row]:
            if x == -1:
                r.append("")
            else:
                r.append("{:.2f}%".format(x))
        cell_text.append(r)

    fig, ax = plt.subplots()
    ax.axis('off')

    table = ax.table(cellText=cell_text,
                     rowLabels=rows,
                     colLabels=columns,
                     loc="center")

    cells = table.get_celld()
    table.auto_set_font_size(False)
    # table.set_fontsize(20)

    print(f'cells {cells}')

    # clear the bottom right cell
    # (average x average)
    # cells[(len(columns), len(rows)-1)]._text.set_text("")

    # increase height of header
    for i in range(len(columns)):
        cells[(0, i)].set_height(0.1)

    plt.title('Failures by algorithm and dataset')
    plt.show()


def Percentage4LeafMapMatchesSummary(raw_result):
    algorithms = readAlgorithms(raw_result)
    small = filterN(raw_results, 6)
    medium = filterN(raw_results, 7)
    large = filterN(raw_results, 8)
    all_sizes = [small, medium, large]
    count = 5
    for j in all_sizes:
        if len(j) <= 0:
            break
        algos = []
        for k in algorithms:
            newalgo = []
            for l in filterAlgorithm(j, str(k)):
                variable = l["Percentage of 4-Leaf Maps Matching Simulation"]
                newalgo.append(round(float(variable.rstrip(" %")), 4))
            algos.append(newalgo)

        x = np.arange(4)  # the label locations
        labels = ['circular\nclockwise', 'circular\nnonclockwise', 'noncircular\nclockwise',
                  'noncircular\nnonclockwise']

        width = 0.1  # the width of the bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - 5 * width / 2, algos[0], width, label='base')
        rects2 = ax.bar(x - 3 * width / 2,
                        algos[1], width, label='realistic-3')
        rects3 = ax.bar(x - width / 2, algos[2], width, label='realistic-4')
        rects4 = ax.bar(x + width / 2, algos[3], width, label='reserve-3')
        rects5 = ax.bar(x + 3 * width / 2, algos[4], width, label='reserve-4')
        rects6 = ax.bar(x + 5 * width / 2, algos[5], width, label='spike')

        ax.set_ylabel('%')
        ax.set_title(
            'Percentage of 4-Leaf-Map matches Simulation on all green paths\nN=' + str(count + 1))
        count += 1
        ax.set_xticks(x, labels)
        ax.legend(loc=1, prop={'size': 7})
        ##plt.savefig(os.path.join(folder_path, 'Percentage_4_leaf_map_matches_simulation' + size_parameter + '.png'), dpi=200)
        plt.show()


def XLeafMapMatchesSummary(raw_results):
    algorithms = readAlgorithms(raw_results)

    small = filterN(raw_results, 6)
    medium = filterN(raw_results, 7)
    large = filterN(raw_results, 8)
    all_sizes = [small, medium, large]
    count = 5
    for j in all_sizes:
        if len(j) <= 0:
            break
        algos = []
        for k in algorithms:
            newalgo = []

            for l in filterAlgorithm(j, str(k)):

                variable = l["Average of random 4-Leaf Maps Matching the Simulation"]
                newalgo.append(variable)
            algos.append(newalgo)
<<<<<<< HEAD
            print(f'----------------{newalgo}')
=======
>>>>>>> 86c68e3fe3f6e2d5b68bc8a29c295fb9c7836e49

        x = np.arange(4)  # the label locations
        labels = ['circular\nclockwise', 'circular\nnonclockwise', 'noncircular\nclockwise',
                  'noncircular\nnonclockwise']

        width = 0.1  # the width of the bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - 5 * width / 2, algos[0], width, label='base')
        rects2 = ax.bar(x - 3 * width / 2,
                        algos[1], width, label='realistic-3')
        rects3 = ax.bar(x - width / 2, algos[2], width, label='realistic-4')
        rects4 = ax.bar(x + width / 2, algos[3], width, label='reserve-3')
        rects5 = ax.bar(x + 3 * width / 2, algos[4], width, label='reserve-4')
        rects6 = ax.bar(x + 5 * width / 2, algos[5], width, label='spike')

<<<<<<< HEAD
        ax.set_ylabel('%')
        ax.set_title('Average of random 4-Leaf Map Matches Simulation\nN=' + str(count + 1))
=======
        ax.set_ylabel('Absolute matched Number')
        ax.set_title(
            'Average of random 4-Leaf-Map matches Simulation\nN=' + str(count + 1))
>>>>>>> 86c68e3fe3f6e2d5b68bc8a29c295fb9c7836e49
        count += 1
        ax.set_xticks(x, labels)
        ax.legend(loc=1, prop={'size': 7})
        ##plt.savefig(os.path.join(folder_path, 'Average_4_leaf_map_matches_Simulation' + size_parameter + '.png'), dpi=200)
        plt.show()


if __name__ == '__main__':
    raw_results = readResults()

    for element in raw_results:
        print(element)

    n_6 = filterN(raw_results, 6)

    print(f'N=6 ({len(n_6)} files)')
    # for element in n_6:
    #    print(element)

    clockwise_results = filterClockwise(raw_results, True)

    print(f'Clockwise True ({len(clockwise_results)} files)')
    # for element in clockwise_results:
    #    print(element)

    n6_clockwise = filterClockwise(n_6, True)
    print(f'Clockwise True and n=6 ({len(n6_clockwise)} files)')
    # for element in n6_clockwise:
    #    print(element)

    base_algo = filterAlgorithm(raw_results, "base")
    print(f'Base algo ({len(base_algo)} files)')

    # TODO do some analysises here
    # e.g. runtime for one dataset comparing the different algorithms

<<<<<<< HEAD
    #percentageCorrectlyClassified(raw_results)
    countPathDistribution(raw_results)
    #failureSummary(raw_results)
    #XLeafMapMatchesSummary(raw_results)
    #Percentage4LeafMapMatchesSummary(raw_results)
=======
    # percentageCorrectlyClassified(raw_results)
    # countPathDistribution(raw_results)
    # failureSummary(raw_results)
    XLeafMapMatchesSummary(raw_results)
    # Percentage4LeafMapMatchesSummary(raw_results)
>>>>>>> 86c68e3fe3f6e2d5b68bc8a29c295fb9c7836e49
