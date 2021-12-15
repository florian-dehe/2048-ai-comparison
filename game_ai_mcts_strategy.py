#Created by Jakub Kachlik
#7.11.2021
#Reimplementation of MCTS algorith for game 2048



from game_functions import  random_move, move_down, move_left, move_right, move_up, add_new_tile
import numpy
import random


POSSIBLE_MOVES = [ move_up, move_left, move_down, move_right]
ORDER = [0,1,2,3]
STATES = [0,0,0,0]


def recursiveSum(move, num_of_levels, board, boardBiggest, originalBoardHighest):
    nboardBiggest = boardBiggest
    nhighestScore = originalBoardHighest
    if num_of_levels > 0:
        random.shuffle(ORDER)
        for index in ORDER:
            newBoard, game_valid, score = POSSIBLE_MOVES[index](board)
            ##print(move, num_of_levels, score)
            if game_valid:
                if numpy.sum(newBoard) > nhighestScore:
                    nboardBiggest = newBoard
                    nhighestScore = numpy.sum(newBoard)
                numOfLevelsNow = num_of_levels - 1
                if numOfLevelsNow > 0:
                    newBoardAdded = add_new_tile(newBoard)
                    resultBoard, resultScore = recursiveSum(move, numOfLevelsNow, newBoardAdded, nboardBiggest, nhighestScore)
                    if numpy.sum(resultBoard) > nhighestScore:
                        nhighestScore = resultScore
                        nboardBiggest = resultBoard
            else:
                continue
    return nboardBiggest, nhighestScore

def recursiveMax(move, num_of_levels, board, boardBiggest, originalBoardHighest):
    nboardBiggest = boardBiggest
    nhighestScore = originalBoardHighest
    if num_of_levels > 0:
        for index in ORDER:
            newBoard, game_valid, score = POSSIBLE_MOVES[index](board)
            ##print(move, num_of_levels, score)
            if game_valid:
                if numpy.amax(newBoard) >= nhighestScore:
                    nboardBiggest = newBoard
                    nhighestScore = numpy.amax(newBoard)
                numOfLevelsNow = num_of_levels - 1
                if numOfLevelsNow > 0:
                    newBoardAdded = add_new_tile(newBoard)
                    resultBoard, resultScore = recursiveMax(move, numOfLevelsNow, newBoardAdded, nboardBiggest, nhighestScore)
                    if numpy.amax(resultBoard) >= nhighestScore:
                        nhighestScore = resultScore
                        nboardBiggest = resultBoard
            else:
                continue
    return nboardBiggest, nhighestScore


def ai_MCTS_strategy(board, num_of_levels):
    BOARD_BIGGEST_SCORE = board
    game_valid_M = True
    moves_score = [0, 0, 0, 0]
    decision= [0, [], board, False]
    for move in POSSIBLE_MOVES:
        ##myBiggestBoard, myHighestScore = recursiveMax(move, num_of_levels, board, BOARD_BIGGEST_SCORE, numpy.amax(board))
        myBiggestBoard, myHighestScore = recursiveSum(move, num_of_levels, board, BOARD_BIGGEST_SCORE, numpy.sum(board))
        STATES[POSSIBLE_MOVES.index(move)] = myBiggestBoard
    
    for state in STATES:
        print(state)
    ##print(bestAction, moves_score)
    ##print(decision[1], decision[0])

    return myBiggestBoard, game_valid_M