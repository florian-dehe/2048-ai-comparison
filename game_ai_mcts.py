#Created by Jakub Kachlik
#7.11.2021
#Reimplementation of MCTS algorith for game 2048


from game_functions import  random_move, move_down, move_left, move_right, move_up, add_new_tile

POSSIBLE_MOVES = [move_left, move_up, move_down, move_right]

def ai_MCTS(board, search_per_move, search_length):
    moves_score = [0, 0, 0, 0]
    for move in POSSIBLE_MOVES:
        newBoard, game_valid, score = move(board)
        if game_valid:
            newBoardAfterFirstMove = add_new_tile(newBoard)
            moves_score[POSSIBLE_MOVES.index(move)] += score
        else:
            continue
        for _ in range(search_per_move):
            newBoard = newBoardAfterFirstMove
            for _ in range(search_length):
                newBoard, game_valid, score = random_move(newBoard)
                if game_valid:
                    newBoard = add_new_tile(newBoard)
                    moves_score[POSSIBLE_MOVES.index(move)] += score
                else:
                    continue

    bestAction = POSSIBLE_MOVES[moves_score.index(max(moves_score))]
    returnBoard, returnGameValid, returnScore = bestAction(board)
    print(bestAction, moves_score)

    return returnBoard, returnGameValid, returnScore