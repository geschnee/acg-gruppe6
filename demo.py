
import erdbeermet.simulation as sim
import erdbeermet.recognition as rec


from inspect import getmembers, isfunction

#befor you can run this you just need to clone the erdbeermet repo and execute in your local copy:
# python setup.py install

N=6
branching_prob=0.5
filename="testfile.txt"

#simulate parameters: https://github.com/david-schaller/Erdbeermet#generation-of-scenarios
scenario = sim.simulate(N, branching_prob)

scenario.print_history() 
#or 
history = scenario.get_history()


print(f'Distances:\n {scenario.distances()}')

print(f'Circular Order: {scenario.get_circular_order()}')

print(f'Writing history to {filename}')
scenario.write_history(filename)

scenario_from_file=sim.load(filename)

print(f'History from {filename}')
scenario_from_file.print_history()
print(f'Distances from {filename}')
print(scenario_from_file.distances())



print("================")
print("recognition")

#recognize: https://github.com/david-schaller/Erdbeermet/blob/main/src/erdbeermet/recognition.py#L334
#from Erdbeermet readme:
recognition_tree = rec.recognize(scenario.D, print_info=True)

# write the recognition steps into a file
recognition_tree.write_to_file('test_recognition.txt')

# visualize the tree (and optionally save the graphic)
recognition_tree.visualize(save_as='test_tree_visualization.pdf')

# print a Newick representation
recognition_tree.to_newick()

