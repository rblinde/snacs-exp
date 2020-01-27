""" Measures accuracy of chosen algorithms against ground truth """

def parse_result(path):
    """ Return communties as list """
    with open(path, "r") as file:
        communities = [str(line.split()[1]) for line in file.readlines()]
        return communities


def calculate(dataset, algorithm, n):
    """ Calculates accuracy for dataset and algorithm """
    ground = parse_result(f"datasets/{dataset}/communities.txt")
    accuracies = list()

    def iteration(i):
        """ Runs once for a particular result file """
        result = parse_result(f"results/result-{dataset}-{algorithm}-{i}.txt")
        # Check equal size
        size = len(ground)
        assert(size == len(result))
        # Actual calculation
        count = 0
        for i in range(size):
            for j in range(i + 1, size):
                eq_ground = ground[i] == ground[j]
                eq_result = result[i] == result[j]
                if eq_ground == eq_result:
                    count = count + 1
        # Checking all possible combinations: N*N
        # Not checking against itself: N*N - N
        # Not checking duplicates: 0.5 * (N*N - N)
        accuracy = (2 * count) / (n * (n-1))
        accuracies.append(accuracy)

    iteration(0)

    if algorithm == "lpa":
        for i in range(1, 10):
            iteration(i)

    avg_acc = round(sum(accuracies) / len(accuracies), 4)
    print(f"Accuracy of '{algorithm}' for '{dataset}': {avg_acc:.4f}")
    print(f"Accuracy of '{algorithm}' for '{dataset}': {avg_acc:.4f}", file=open("result.txt", "a"))


def main():
    sizes = {
        "corporate-small": 1689,
        "corporate": 328574,
    }
    datasets = ["corporate-small", "corporate"]

    for dataset in datasets:
        calculate(dataset, "gm", sizes[dataset])
        calculate(dataset, "gn", sizes[dataset])
        calculate(dataset, "lpa", sizes[dataset])
    print(f"=" * 40, file=open("result.txt", "a"))


if __name__ == "__main__":
    main()
