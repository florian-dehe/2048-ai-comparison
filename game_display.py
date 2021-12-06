'''

MIT License

Copyright (c) 2020 Kite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


from tkinter import Frame, Label, CENTER

import game_ai_mcts
import game_ai_random
import game_ai_qlearning
import game_ai_GA
import game_functions
import time
import game_ai_nn

EDGE_LENGTH = 400
CELL_COUNT = 4
CELL_PAD = 10

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY= "'d'"
KEY_TABLE = [ UP_KEY, DOWN_KEY, LEFT_KEY, RIGHT_KEY ]
AI_MCTS = "'m'"
AI_Q_LEARNING_START = "'q'"
AI_RANDOM = "'r'"
AI_INIT = "'i'"
AI_NN = "'n'"
AI_NN_TRAINING = "'t'"

LABEL_FONT = ("Verdana", 40, "bold")

GAME_COLOR = "#c2b3a9"

EMPTY_COLOR = "#a39489"

TILE_COLORS = {    
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#f0b922",
    2048: "#fad74d"}

LABEL_COLORS = {    
    2: "#695c57",
    4: "#695c57",
    8: "#ffffff",
    16: "#ffffff",
    32: "#ffffff",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff"}

class Display(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: game_functions.move_up, 
                         DOWN_KEY: game_functions.move_down,
                         LEFT_KEY: game_functions.move_left, 
                         RIGHT_KEY: game_functions.move_right,
                         }

        self.nn_training = False
        
        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()

        self.mainloop()

    def build_grid(self):
        background = Frame(self, bg=GAME_COLOR,
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()

        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(background, bg=EMPTY_COLOR,
                             width=EDGE_LENGTH / CELL_COUNT,
                             height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                t = Label(master=cell, text="",
                          bg=EMPTY_COLOR,
                          justify=CENTER, font=LABEL_FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()

    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=TILE_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value])
        self.update_idletasks()
    
    def key_press(self, event):

        key = repr(event.char)
        if key == AI_MCTS:
            game_valid = True
            while game_valid:
                self.matrix, game_valid, gameScore = game_ai_mcts.ai_MCTS(self.matrix, 40, 10)
                if game_valid:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                    print(self.matrix)
                    print("")

        elif key == AI_RANDOM:
            game_valid = True
            while game_valid:
                self.matrix, game_valid = game_ai_random.randomMove(self.matrix)
                if game_valid:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells
                    print(self.matrix)
                    print("")
                elif game_valid == False:
                    self.draw_grid_cells()

        elif key == AI_Q_LEARNING_START:
            game_valid = True
            q_table = game_ai_qlearning.QTable( exploration_chance=0.1, 
                                                gamma_value=0.9, 
                                                learning_rate=0.15, 
                                                action_range=4)
            while game_valid:
                self.matrix, game_valid = game_ai_qlearning.ai_q_learning(self.matrix, q_table)
                if game_valid:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                    print(self.matrix)
                    print("")
                else:
                    print("Reset !")
                    self.matrix = game_functions.initialize_game()
                    self.draw_grid_cells()
                    game_valid = True
        
        elif key == AI_NN:
            game_valid = True
            if len(self.nn_training_dataset) == 0:
                print("No training data for Neural Network !")
                return
            
            if self.nn_training:
                print("Still training for Neural Network !")
                return

            net = game_ai_nn.ANN(16, 32, 4)
            print("Training neural network...")
            net.train(self.nn_training_dataset, 200)
            print("Neural network trained !")
            
            #Clear board
            self.matrix = game_functions.initialize_game()
            self.draw_grid_cells()

            game_valid = True
            
            while game_valid:
                outputs = net.compute(game_ai_nn.matrix_to_list(self.matrix))
                index = 0
                for i in range(len(outputs)):
                    if outputs[i] == 1:
                        index = i
                        break
                print("Prediction:", KEY_TABLE[index])
                move_command = self.commands[KEY_TABLE[index]]
                self.matrix, game_valid, score = move_command(self.matrix)
                if not game_valid:
                    board, move_possible = game_functions.fixed_move(self.matrix)
                    if not move_possible:
                        break
                    game_valid = move_possible
                    self.matrix = board
                
                print(self.matrix)
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()

            print("End neural network")

        elif key == AI_NN_TRAINING:
            self.nn_training = not self.nn_training
            if self.nn_training:
                self.nn_training_dataset = [ ]
                print("Neural network training enabled !")
            else:
                print("Neural network training disabled !")
                print("Training data set length :",  len(self.nn_training_dataset))

        elif key == AI_INIT:
            self.matrix = game_functions.initialize_game()
            self.draw_grid_cells()

        elif key in self.commands:
            move_key_name = repr(event.char)
            self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False
                if self.nn_training:
                    targets = [ 0, 0, 0, 0 ]
                    targets[KEY_TABLE.index(move_key_name)] = 1
                    data = game_ai_nn.DataSet(game_ai_nn.matrix_to_list(self.matrix), targets )
                    print("Training data :", data.values, data.targets)
                    self.nn_training_dataset.append(data)
                
gamegrid = Display()
