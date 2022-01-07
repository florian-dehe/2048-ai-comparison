# 2048-ai-comparison

Comparison of different AI techniques solving the 2048 game

## Installation :
This project runs under Python 3 (tested 3.9 and 3.10)

It uses the given libraries : `numpy` and `tkinter`. Make sure there installed with `pip3 list` or `pip3 show <package>`. If they are not, use `pip3 install <package>`

## Usage :
To launch the main program, use : `python3 game_display.py`

Here is a list of the key commands that can be useful :

| Key | Command |
|-----|---------|
| `W` | UP_KEY  |
| `S` | DOWN_KEY |
| `A` | LEFT_KEY |
| `D` | RIGHT_KEY |
| `I` | INIT (re-init the board) |
| `M` | AI_MCTS (score)|
| `B` | AI_MCTS2 (sum) |
| `V` | AI_MCTS3 (max) |
| `Q` | AI_Q_LEARNING |
| `R` | AI_RANDOM |
| `T` | AI_NN_TRAINING (toggle) |
| `N` | AI_NN (after training !) |

**Note :** Every AI Algorithm stops when the game is stuck (not when reaching 2048 !)
