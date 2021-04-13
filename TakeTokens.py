#!/usr/bin/python
import sys
import getopt
# from Heuristic import static_board_evaluation

def seq_check(size, lst_taken) -> bool:
    '''Check for correctness of ordered sequence'''

    full_lst = [i for i in range(1 , size + 1)]
    if lst_taken[0] < -(size // -2): # first move is odd-numbered token that is strictly less than n/2
        last_elem = lst_taken[0]
        full_lst.remove(last_elem)
        for e in lst_taken[1:]:
            # subsequent moves must be a multiple or factor of the last move
            if  (e % last_elem == 0) or (last_elem % e == 0): 
                last_elem = e
                if e in full_lst:
                    full_lst.remove(e)
                else:
                    return False
            else:
                return False
        return True
    return False


def main(argv):
    '''Parse command-line input and construct pruning object'''
    
    try:
        # simulate help display
        opts, _ = getopt.getopt(argv,"h", ["help"])
        for opt, _ in opts:
            if opt == '-h' or opt == '--help':
                print('usage: TakeTokens.py [-h] [Tokens] [Taken] N [N ...] [Depth]\n\n'
                      'Compute the best move for the current player using Alpha-Beta pruning algorithm\n'
                      'to play a two-player game called PNT: pick numbered-tokens\n\n'
                      'positional arguments:\n'
                      'Tokens       Total number of tokens in the game\n'
                      'Taken        Number of tokens that have already been taken in previous moves\n'
                      '             If this number is 0, this is the first move in a game, which will be played by Max.\n'
                      'N            Sequence of integers indicating the indexes of the already taken tokens,\n'
                      '             ordered from first to last token taken. If N is 0, this list will be empty.\n'
                      'Depth        Search depth. If depth is 0, search to end game states \n'
                      '             (i.e., states where a winner is determined).')
                return
        
        # parse params
        tokens = int(argv[0])
        taken_tokens = int(argv[1])
        assert(len(argv) > 2)
        if taken_tokens != 0:
            lst_taken_token = list(map(int, argv[2:-1]))
            assert(len(lst_taken_token) == taken_tokens)
            assert(seq_check(tokens, lst_taken_token))
        depth = int(argv[-1])

    except:
        print('usage: TakeTokens.py [-h] [Tokens] [Taken_tokens] N [N ...] [Depth]')
        print('TakenTokens.py: error: invalid format')
        sys.exit(2)

    # TODO 
    # what do we do with those params?
    # analysis.py for 10 random testcase
    player = 'Max' if taken_tokens % 2 == 0 else 'Min'
    print(player, tokens, taken_tokens, lst_taken_token, depth)

  

if __name__ == "__main__":
    main(sys.argv[1:])