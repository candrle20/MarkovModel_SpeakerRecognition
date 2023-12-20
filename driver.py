import sys
from markov import identify_speaker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    #Open files & read text
    textA = open(filenameA, 'r').read()
    textB = open(filenameB, 'r').read()
    textC = open(filenameC, 'r').read()

    #Call identify_speaker & print results
    speakerA, speakerB, ans = identify_speaker(textA, textB, textC, k, hashtable_or_dict)
    print()
    print("Speaker A:", speakerA)
    print("Speaker B:", speakerB)
    print()
    print(f"Conclusion: Speaker {ans} is most likely")
    print()