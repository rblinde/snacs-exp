import time
import networkx as nx
from networkx.algorithms import community
from collections import defaultdict

def write_to_file(name, communities):
    sequence = {}

    for i, c in enumerate(communities):
        for node in list(c):
            sequence[int(node)] = i

    # sequence = sorted(list(sequence.items()))
    sequence = list(sequence.items())
    sequence = [f"{i[0]} {i[1]}\n" for i in sequence]

    with open(name, "w") as file:
        file.writelines(sequence)

def coms_normal(result):
    return [set(x) for x in result]

def coms_gen(result):
    return [set(x) for x in next(result)]

def run(dataset, name, algorithm, fn):
    G = nx.read_edgelist(f"datasets/{dataset}/edges.txt")
    start = time.time()
    result = algorithm(G)
    middle = time.time()
    communities = fn(result)
    end = time.time()
    run_time = round((end - start) * 1000, 6)
    middle_time = round((middle - start) * 1000, 6)
    print(f"RTime | {name} | {dataset} | {run_time}", file=open("times.txt", "a"))
    print(f"MTime | {name} | {dataset} | {middle_time}", file=open("times.txt", "a"))

    write_to_file(f"result-{dataset}-{name}.txt", communities)
    # Output
    print(f"Dataset {dataset} completed for algorithm {name}!")
    

if __name__ == '__main__':
    for dataset in ["amazon", "youtube"]:
        run(dataset, "gn", community.girvan_newman, coms_gen)
        run(dataset, "gm", community.greedy_modularity_communities, coms_normal)
