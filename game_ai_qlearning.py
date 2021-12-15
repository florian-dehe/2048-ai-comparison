
import random
import math
import time
import numpy as np

from game_functions import check_for_win, fixed_move, move_down, move_left, move_right, move_up, add_new_tile

class QTable:
    def __init__(self, exploration_chance, gamma_value, learning_rate, action_range):
        self.exploration_chance = exploration_chance
        self.gamma_value = gamma_value
        self.learning_rate = learning_rate

        self.table = { }
        self.action_range = action_range
        self.prev_state = ""
        self.prev_action = 0
    
    # Get the next action (e-greedy action)
    def get_next_action(self, matrix):
        self.prev_state = matrix

        if random.random() < self.exploration_chance :
            self.prev_action = self.explore()
        else:
            self.prev_action = self.get_best_action(matrix)
        
        return self.prev_action
    
    # Get the best action based on q values
    def get_best_action(self, matrix):
        q_values = self.get_actions_q_values(matrix)
        best_actions = [ ]
        best_value = -math.inf
        for i in range(len(q_values)):
            if q_values[i] > best_value:
                best_value = q_values[i]
                best_actions = [ ]
                best_actions.append(i)
            elif q_values[i] == best_value:
                best_actions.append(i)
        return best_actions[random.randint(0, len(best_actions)-1)]

    # Random action selection (in this case 4)
    def explore(self):
        return random.randint(0, self.action_range-1)

    def update_q_value(self, reward, matrix):
        q_values = self.get_actions_q_values(matrix)
        best_value = -math.inf
        for i in range(len(q_values)):
            if q_values[i] > best_value:
                best_value = q_values[i]
        
        prev_q_values = self.get_actions_q_values(self.prev_state)
        prev_q_value_for_action = prev_q_values[self.prev_action]

        new_q_value = prev_q_value_for_action + self.learning_rate + (reward + self.gamma_value * best_value - prev_q_value_for_action)
        self.table[self.get_matrix_string(self.prev_state)][self.prev_action] = new_q_value

    def get_matrix_string(self, matrix):
        result = ""
        for y in range(len(matrix)):
            for x  in range(len(matrix[0])):
                result += "" + str(matrix[y][x])
        return result
    
    def get_actions_q_values(self, matrix):
        actions = self.get_values(matrix)
        if actions == None:
            initial_actions = [ ]
            for i in range(self.action_range):
                initial_actions.append(0)
            self.table[self.get_matrix_string(matrix)] = initial_actions
            return initial_actions
        return actions
    
    def print_q_table(self):
        for k, values in enumerate(self.table):            
            key = str(k)
            print(key[0], "",  key[1],  "",  key[2])
            print("  UP   RIGHT  DOWN  LEFT")
            print(key[3], "", key[4], "", key[5])
            print(": ", values[0], "   ", values[1], "   ", values[2], "   ", values[3])
            print(key[6], "", key[7], "", key[8])
            

    def get_values(self, matrix):
        matrix_key = self.get_matrix_string(matrix)

        if matrix_key in self.table.keys():
            return self.table[matrix_key]
        else:
            return None
        
def ai_q_learning(matrix, q_table : QTable):
    ACTIONS = [ move_up, move_right , move_down, move_left ]

    mat, game_valid = fixed_move(matrix)
    if not game_valid:
        return matrix, game_valid

    game_valid = False
    while not game_valid:
        action = q_table.get_next_action(matrix)
        print(ACTIONS[action])
        new_matrix, game_valid, score = ACTIONS[action](matrix)
    
    reward = np.max(new_matrix)
    q_table.update_q_value(reward, new_matrix)
    #q_table.print_q_table()
    
    time.sleep(0.1)
    return new_matrix, game_valid
