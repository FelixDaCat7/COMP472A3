import argparse
import numpy as np
import os
import TakeTokens

def main(args):
    """
    Analyse and compare the performance of the game using input testcases.
    """
    results = [] # list of all results
    with args.i as f:  # read input file
        for line in f:  # Add input puzzles into puzzle list
            inputs = line.strip().split()[1:]
            results.append(np.array(TakeTokens.main(inputs)))
    results = np.array(results)
    print(results)

            
if __name__ == "__main__":
    """
    Parse command line argument for the input file
    """
    parser = argparse.ArgumentParser(description='Generate an analysis for the Alpha-Beta pruning algorithm')
    parser.add_argument('-i', metavar='FILENAME', required=True,
                        type=argparse.FileType('r'),
                        help='filename of the inputs')
    args = parser.parse_args()
    main(args)
