# last_move: integer
# remaining_tokens: list of integers
# is_max_turn: boolean, max turn (true), min turn (false)

# print(static_board_evaluation(5, [3, 2, 6, 8, 10, 11], True))
def static_board_evaluation(last_move: int, remaining_tokens: list[int], is_max_turn: bool) -> float:
    if is_end_game(last_move, remaining_tokens):
        evaluation = 1
    else:
        evaluation = get_evaluation(last_move, remaining_tokens)
    if is_max_turn:
        return evaluation
    else:
        return -evaluation


def is_end_game(last_move: int, remaining_tokens: list[int]) -> bool:
    for token in remaining_tokens:
        if last_move % token == 0 or token % last_move == 0:
            return False
    return True


def is_prime(possibly_prime: int) -> bool:
    is_prime_number = True
    for integer in range(2, possibly_prime):
        if possibly_prime % integer == 0:
            is_prime_number = False
            break
    return is_prime_number


def get_evaluation(last_move: int, remaining_tokens: list[int]) -> float:
    # case 1: 1 is still in remaining tokens
    for token in remaining_tokens:
        if token == 1:
            return 1
    # case 2: 1 is the last move
    if last_move == 1:
        if len(remaining_tokens) % 2 != 0:
            return 0.5
        else:
            return -0.5
    # case 3: last move is prime
    if is_prime(last_move):
        multiple_count = 0
        for token in remaining_tokens:
            if token % last_move == 0:
                multiple_count = multiple_count + 1
        if multiple_count % 2 != 0:
            return 0.7
        else:
            return -0.7
    # case 4: last move is composite
    prime_divider = 0
    for integer in range(2, last_move):
        if last_move % integer == 0:
            if is_prime(integer):
                prime_divider = integer
    multiples_count = 0
    for integer in remaining_tokens:
        if integer % prime_divider == 0:
            multiples_count = multiples_count + 1
    if multiples_count % 2 != 0:
        return 0.6
    else:
        return -0.6
