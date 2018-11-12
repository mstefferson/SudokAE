import SudokuMaster
import numpy as np
import os
import logging
import argparse


class PuzzelBuilder():
    def __init__(self, num_puzzles, logger=None):
        # build the logger if it's not passed
        if not logger:
            self.logger = build_logger('puzzle_build')
        else:
            self.logger = logger
        num_puzzles = int(num_puzzles)
        self.main_dir = os.getcwd()
        self.data_dir = self.main_dir + '/data/'
        self.valid_puzzle_types = set(['solved', 'easy',
                                       'moderate', 'difficult'])
        self.solved_path = self.data_dir
        self.num_puzzles = int(num_puzzles)
        # set up str for saving
        num_zeros = str(int(np.log10(num_puzzles)))
        self.puzzle_name = 'puzzle_{:0' + num_zeros + 'd}'

    def build_dir(self, dir_name):
        os.makedirs(dir_name, exist_ok=True)

    def build_data_dirs(self):
        self.build_dir(self.data_dir)
        for mdir in self.valid_puzzle_types:
            mdir2build = self.data_dir + mdir + '/'
            self.build_dir(mdir2build + 'x')
            self.build_dir(mdir2build + 'y')

    def make_all_puzzels(self):
        for puzzle in self.valid_puzzle_types:
            self.make_puzzle_data(puzzle)

    def make_puzzle_data(self, puzzle_type):
        dir2save = self.get_puzzle_dir(puzzle_type)
        # build all the puzzles and solutions
        self.logger.info('Building puzzles for type ' + puzzle_type)
        for i in range(self.num_puzzles):
            save_name = self.puzzle_name.format(i) + '.txt'
            p, b = self.make_puzzle_pair(puzzle_type)
            # save them in x and y
            np.savetxt(dir2save + 'x/' + save_name, p, fmt='%d')
            np.savetxt(dir2save + 'y/' + save_name, b, fmt='%d')

    def make_puzzle_pair(self, puzzle_type):
        if puzzle_type not in self.valid_puzzle_types:
            raise ValueError(puzzle_type +
                             ' is an unknown puzzle type, will break')
        # build board
        board = SudokuMaster.makeBoard()
        # make a copy of the board
        board_store = [list(r) for r in board]
        if puzzle_type == 'solved':
            puzzle = board
        else:
            puzzle = SudokuMaster.makePuzzleBoard(board, puzzle_type)
        return puzzle, board_store

    def get_puzzle_dir(self, puzzle_type):
        if puzzle_type not in self.valid_puzzle_types:
            raise ValueError(puzzle_type +
                             ' is an unknown puzzle type, this will break')
        return self.data_dir + puzzle_type + '/'


def build_logger(log_name='puzz_build'):
    # set-up logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_name+'.log', mode='w')
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def main(args):
    # get logger
    logger = build_logger()
    # make a puzzle builder
    puzz_builder = PuzzelBuilder(args.num_puzz, logger)
    logger.info('Initialized puzzle builder ')
    # build puzzle directories
    puzz_builder.build_data_dirs()
    logger.info('Built data directories')
    # build puzzles
    if args.puzzle == 'all':
        puzz_builder.make_all_puzzels()
    else:
        puzz_builder.make_puzzle_data(args.puzzle)
    log_str = 'Built ' + args.puzzle + ' puzzles'
    logger.info(log_str)
    log_str = 'Built ' + args.num_puzz + ' per puzzle type'
    logger.info(log_str)


if __name__ == '__main__':
    '''
    Executeable:
    '''
    # set-up arg parsing
    argparser = argparse.ArgumentParser(
        description='Builds data set of sudoku puzzels')
    argparser.add_argument(
        '-p',
        '--puzzle',
        default='all',
        help='Type of puzzels')
    argparser.add_argument(
        '-n',
        '--num_puzz',
        help='number of puzzles')
    args = argparser.parse_args()
    main(args)
