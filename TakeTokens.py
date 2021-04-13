#!/usr/bin/python
import sys
import getopt
# from Heuristic import static_board_evaluation

def main(argv):
    try:
        # simulate help display
        opts, _ = getopt.getopt(argv,"h", ["help"])
        for opt, _ in opts:
            if opt == '-h' or opt == '--help':
                print('usage: TakeTokens.py [-h] [Tokens] [Taken] N [N ...] [Depth]')
                print('positional arguments:\n'
                      'Tokens       Total number of tokens in the game\n'
                      'Taken        Number of tokens that have already been taken in previous moves\n'
                      '             If this number is 0, this is the first move in a game, which will be played by Max.\n'
                      'N            Sequence of integers indicating the indexes of the already taken tokens,\n'
                      '             ordered from first to last token taken. If N is 0, this list will be empty.\n'
                      'Depth        Search depth. If depth is 0, search to end game states \n'
                      '             (i.e., states where a winner is determined).')
                sys.exit()
        
        # parse params
        tokens = int(argv[0])
        taken_tokens = int(argv[1])
        if taken_tokens != 0:
            lst_taken_token = list(map(int, argv[2:-1]))
            assert(len(lst_taken_token) == taken_tokens)
        depth = int(argv[-1])

    except:
        print('usage: TakeTokens.py [-h] [Tokens] [Taken_tokens] N [N ...] [Depth]')
        print('TakenTokens.py: error: invalid format')
        sys.exit(2)

    # TODO process params
    print(tokens, taken_tokens, lst_taken_token, depth)
    # print(static_board_evaluation(5, [3, 2, 6, 8, 10, 11], True))

if __name__ == "__main__":
    main(sys.argv[1:])








