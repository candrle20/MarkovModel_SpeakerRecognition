import sys
from markov import identify_speaker
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)
    textA = open(filenameA, 'r').read()
    textB = open(filenameB, 'r').read()
    textC = open(filenameC, 'r').read()

    #Performance Testing
    results = []

    for k in range(1, max_k + 1):
        for run in range(1, runs + 1):
            for implementation in ['Hashtable', 'Dictionary']:
                start = time.perf_counter()
                identify_speaker(textA, textB, textC, k, use_hashtable=(implementation == 'Hashtable'))
                total = time.perf_counter() - start
                results.append({'Implementation': implementation, 'K': k, 'Run': run, 'Time': total})

    df = pd.DataFrame(results)

    #Average Run Time by K and Implementation
    avg_time = df.groupby(['Implementation', 'K']).mean().reset_index()

    #Seaborn Graph
    sns.pointplot(data=avg_time, x='K', y='Time', hue='Implementation', linestyle='-', marker='o')
    plt.xlabel('K')
    plt.ylabel(f'Average Run Time (s) (Runs: {runs})')
    plt.title('Hashtable vs Python Dict Performance')
    plt.savefig('execution_graph.png')