import SudokuMaster
import numpy as np

board = SudokuMaster.makeBoard()
np.savetxt('board1.txt', board, fmt='%d')
