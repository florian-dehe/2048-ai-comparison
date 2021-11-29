
from game_functions import  random_move, move_down, move_left, move_right, move_up, add_new_tile

POSSIBLE_MOVES = [move_left, move_up, move_down, move_right]

def generation_algorithm (board, number_of_genoms, length_of_genom):
    genoms = []
    for _ in range(number_of_genoms):
        genome = []
        scoreTotal = 0
        gameBoard = board
        for _ in range(length_of_genom):
            newBoard, game_valid, score = random_move(gameBoard)
            if game_valid:
                scoreTotal += score
                gameBoard = add_new_tile(newBoard)
        genoms.append(scoreTotal)
    
    print(genoms)
    return board