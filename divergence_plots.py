import matplotlib.pyplot as plt
import numpy as np
import yaml
import os

def read_file(folder_name, benchmark_file):
    with open(os.path.join(os.getcwd(), folder_name, benchmark_file), "r") as stream:
        try:
            dict = yaml.safe_load(stream)
            return dict
        except yaml.YAMLError as exc:
            print(exc)

def get_files(path):
    files = os.listdir(path)
    return files

def get_data(folder_name, size_parameter = 'small'):
    files = get_files(os.path.join(os.getcwd(), folder_name))
    ccw = []
    nccw = []
    cncw = []
    ncncw = []
    for f in files:
        if str(size_parameter + '_circular_clockwise') in f:
            ccw.append(f)
        if str(size_parameter + '_circular_nonclockwise') in f:
            cncw.append(f)
        if str(size_parameter + '_noncircular_clockwise') in f:
            nccw.append(f)
        if str(size_parameter + '_noncircular_nonclockwise') in f:
            ncncw.append(f)
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    ct1 = []
    ct2 = []
    ct3 = []
    ct4 = []
    co1 = []
    co2 = []
    co3 = []
    co4 = []
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    for f in ccw:
        dict = read_file(folder_name, f)
        x1.append(dict['Algorithm'])
        ct1.append(dict['Percentage of common triples'])
        co1.append(dict['Average Number of co-optimal solutions'])
        t1.append(dict['Average duration time'])
    for f in nccw:
        dict = read_file(folder_name, f)
        x2.append(dict['Algorithm'])
        ct2.append(dict['Percentage of common triples'])
        co2.append(dict['Average Number of co-optimal solutions'])
        t2.append(dict['Average duration time'])
    for f in cncw:
        dict = read_file(folder_name, f)
        x3.append(dict['Algorithm'])
        ct3.append(dict['Percentage of common triples'])
        co3.append(dict['Average Number of co-optimal solutions'])
        t3.append(dict['Average duration time'])
    for f in ncncw:
        dict = read_file(folder_name, f)
        x4.append(dict['Algorithm'])
        ct4.append(dict['Percentage of common triples'])
        co4.append(dict['Average Number of co-optimal solutions'])
        t4.append(dict['Average duration time'])

    x = [x1, x2, x3, x4]
    ct = [ct1, ct2, ct3, ct4]
    co = [co1, co2, co3, co4]
    t = [t1, t2, t3, t4]

    return x, ct, co, t

def common_triples_plot(folder_name, folder_path, size_parameter = 'small'):
    x, ct, co, t = get_data(folder_name, size_parameter)

    base = [0 for i in range(4)]                         # base[0] is value for data for ccw for example
    realistic3 = [0 for i in range(4)]
    realistic4 = [0 for i in range(4)]
    reserve3 = [0 for i in range(4)]
    reserve4 = [0 for i in range(4)]
    spike = [0 for i in range(4)]
    for index in range(0, len(x)):                     # for each parameter --> index = param
        for jdex in range(0, len(x[index])):           # for each algorithm --> jdex = alg
            if x[index][jdex] == 'base':
                base[index] = float(ct[index][jdex].split('%')[0])         # co[index] gives co1 - array with 6 values,
            if x[index][jdex] == 'realistic-3':
                realistic3[index] = float(ct[index][jdex].split('%')[0])
            if x[index][jdex] == 'realistic-4':
                realistic4[index] = float(ct[index][jdex].split('%')[0])
            if x[index][jdex] == 'reserve-3':
                reserve3[index] = float(ct[index][jdex].split('%')[0])
            if x[index][jdex] == 'reserve-4':
                reserve4[index] = float(ct[index][jdex].split('%')[0])
            if x[index][jdex] == 'spike':
                spike[index] = float(ct[index][jdex].split('%')[0])

    labels = ['ccw', 'nccw', 'cncw', 'ncncw']
    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 5 * width/2, base, width, label = 'base')
    rects2 = ax.bar(x - 3 * width / 2, realistic3, width, label='realisitc3')
    rects3 = ax.bar(x - width / 2, realistic4, width, label='realistic4')
    rects4 = ax.bar(x + width / 2, reserve3, width, label='reserve3')
    rects5 = ax.bar(x + 3 * width / 2, reserve4, width, label='reserve4')
    rects6 = ax.bar(x + 5 * width / 2, spike, width, label='spike')

    ax.set_ylabel('%')
    ax.set_title('Percentage of common triplets by parameters and Algorithm')
    ax.set_xticks(x, labels)
    ax.legend(loc = 4, prop={'size': 7})
    plt.savefig(os.path.join(folder_path, 'commontriples_' + size_parameter + '.png'), dpi = 200)
    plt.show()

def co_optimal_plot(folder_name, folder_path, size_parameter = 'small'):
    x, ct, co, t = get_data(folder_name, size_parameter)

    base = [0 for i in range(4)]  # base[0] is value for data for ccw for example
    realistic3 = [0 for i in range(4)]
    realistic4 = [0 for i in range(4)]
    reserve3 = [0 for i in range(4)]
    reserve4 = [0 for i in range(4)]
    spike = [0 for i in range(4)]
    for index in range(0, len(x)):  # for each parameter --> index = param
        for jdex in range(0, len(x[index])):  # for each algorithm --> jdex = alg
            if x[index][jdex] == 'base':
                base[index] = float(co[index][jdex])  # co[index] gives co1 - array with 6 values,
            if x[index][jdex] == 'realistic-3':
                realistic3[index] = float(co[index][jdex])
            if x[index][jdex] == 'realistic-4':
                realistic4[index] = float(co[index][jdex])
            if x[index][jdex] == 'reserve-3':
                reserve3[index] = float(co[index][jdex])
            if x[index][jdex] == 'reserve-4':
                reserve4[index] = float(co[index][jdex])
            if x[index][jdex] == 'spike':
                spike[index] = float(co[index][jdex])

    labels = ['ccw', 'nccw', 'cncw', 'ncncw']
    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 5 * width / 2, base, width, label='base')
    rects2 = ax.bar(x - 3 * width / 2, realistic3, width, label='realisitc3')
    rects3 = ax.bar(x - width / 2, realistic4, width, label='realistic4')
    rects4 = ax.bar(x + width / 2, reserve3, width, label='reserve3')
    rects5 = ax.bar(x + 3 * width / 2, reserve4, width, label='reserve4')
    rects6 = ax.bar(x + 5 * width / 2, spike, width, label='spike')

    ax.set_ylabel('Number of paths')
    ax.set_title('Average number of co-optimal solutions')
    ax.set_xticks(x, labels)
    ax.legend(loc=1, prop={'size': 7})
    plt.savefig(os.path.join(folder_path, 'cooptimal_' + size_parameter + '.png'), dpi = 200)
    plt.show()

def runtime_plot(folder_name, folder_path, size_parameter = 'small'):
    x, ct, co, t = get_data(folder_name, size_parameter)

    base = [0 for i in range(4)]  # base[0] is value for data for ccw for example
    realistic3 = [0 for i in range(4)]
    realistic4 = [0 for i in range(4)]
    reserve3 = [0 for i in range(4)]
    reserve4 = [0 for i in range(4)]
    spike = [0 for i in range(4)]
    for index in range(0, len(x)):  # for each parameter --> index = param
        for jdex in range(0, len(x[index])):  # for each algorithm --> jdex = alg
            if x[index][jdex] == 'base':
                base[index] = float(t[index][jdex])  # co[index] gives co1 - array with 6 values,
            if x[index][jdex] == 'realistic-3':
                realistic3[index] = float(t[index][jdex])
            if x[index][jdex] == 'realistic-4':
                realistic4[index] = float(t[index][jdex])
            if x[index][jdex] == 'reserve-3':
                reserve3[index] = float(t[index][jdex])
            if x[index][jdex] == 'reserve-4':
                reserve4[index] = float(t[index][jdex])
            if x[index][jdex] == 'spike':
                spike[index] = float(t[index][jdex])

    labels = ['ccw', 'nccw', 'cncw', 'ncncw']
    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 5 * width / 2, base, width, label='base')
    rects2 = ax.bar(x - 3 * width / 2, realistic3, width, label='realisitc3')
    rects3 = ax.bar(x - width / 2, realistic4, width, label='realistic4')
    rects4 = ax.bar(x + width / 2, reserve3, width, label='reserve3')
    rects5 = ax.bar(x + 3 * width / 2, reserve4, width, label='reserve4')
    rects6 = ax.bar(x + 5 * width / 2, spike, width, label='spike')

    ax.set_ylabel('Seconds')
    ax.set_title('Average duration time per hfile')
    ax.set_xticks(x, labels)
    ax.legend(loc=2, prop={'size': 7})
    plt.savefig(os.path.join(folder_path, 'runtime_' + size_parameter + '.png'), dpi = 200)
    plt.show()

if __name__ == '__main__':
    folder_path = os.path.join(os.getcwd(), 'result_plots')
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    runtime_plot('final_results', folder_path)
    common_triples_plot('final_results', folder_path)
    co_optimal_plot('final_results', folder_path)







