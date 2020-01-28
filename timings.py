""" Measures average running time of algorithms """

import time
import networkx as nx
from networkx.algorithms import community

def coms_normal(result):
    return [set(x) for x in result]


def coms_gen(result):
    return [set(x) for x in next(result)]


def run(dataset, name, algorithm, fn):
    """ Measure time from start to list result in ms """
    def iteration(i):
        start = time.time()
        result = algorithm(G)
        _ = fn(result)
        end = time.time()
        run_time = round((end - start) * 1000, 6)
        return run_time

    G = nx.read_edgelist(f"datasets/{dataset}/edges.txt")
    times = []

    for i in range(10):
        times.append(iteration(i))

    avg_time = sum(times) / len(times)
    print(f"Time | {name} | {dataset} | {avg_time}")
    print(f"Time | {name} | {dataset} | {avg_time}", file=open("timings-only.txt", "a"))


if __name__ == '__main__':
    for dataset in ["karate", "football", "email", "corporate-small", "corporate"]:
        run(dataset, "lpa", community.asyn_lpa_communities, coms_normal)
        run(dataset, "gm", community.greedy_modularity_communities, coms_normal)
        if dataset is not "corporate":
            run(dataset, "gn", community.girvan_newman, coms_gen)
        print("=" * 50, file=open("timings-only.txt", "a"))
