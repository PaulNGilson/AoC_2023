from collections import defaultdict
import random, copy
import sys

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

# use Karger's algorithm next - in brief: unify vertices by randomly selecting
# an edge, update all vertices to connect to this new unified vertex and repeat
# until two vertices remain - the edges between them is an attempted guess of
# k-connectivity (in this challenge, we know k=3 so quit when found)

components = defaultdict(list)

# build our bi-directional/undirected dictionary representing the graph
for line in data:
    component_origin, component_destinations_str = line.split(": ")
    component_destinations = component_destinations_str.split(" ")
    for component_destination in component_destinations:
        components[component_origin].append(component_destination)
        components[component_destination].append(component_origin)

def karger(current_components):
    length = []
    while len(current_components.keys()) > 2: # keep reducing until we have just 2 vertices left
        # randomly choose an edge - in theory, we're less likely to choose the
        # min-cut ones as they are few
        vertex1 = random.choice(list(current_components.keys()))
        vertex2 = random.choice(list(current_components[vertex1]))
        vertex1_destinations_to_keep = [d for d in current_components[vertex1] if d != vertex2]
        vertex2_destinations_to_keep = [d for d in current_components[vertex2] if d != vertex1]

        # create destinations (essentially edges) for our new combined vertex
        new_destinations = vertex1_destinations_to_keep + vertex2_destinations_to_keep

        # remove the old vertices
        del current_components[vertex1]
        del current_components[vertex2]

        # add the new one - just give it a string concatenation name *which*
        # we'll use later on to determine just how many vertices made up each group
        # in the end (we rely upon all names just being three letters long)
        new_vertex = vertex1 + vertex2
        current_components[new_vertex] = new_destinations

        # update all the others
        for component in current_components.keys():
            current_components[component] = [v if v not in [vertex1, vertex2] else new_vertex for v in current_components[component]]
    for component in current_components.keys():
        length.append(len(current_components[component]))
    return length[0], current_components

k = sys.maxsize
final_kargerified_components = {}
while k > 3: # stop when we get to 3-connectivity
    new_components = copy.deepcopy(components)
    k, final_kargerified_components = karger(new_components)
total = 1
for origin in final_kargerified_components:
    total *= len(final_kargerified_components[origin][0]) / 3
print("part 1:", int(total))

# part 2 begins...
# <push big red button>
# ...and ends!
