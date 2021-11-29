#Created by Jakub Kachlik
#7.11.2021
#Random move game agent


from game_functions import  random_move

def randomMove(board):
    newBoard, game_valid, score = random_move(board)

    return newBoard, game_valid