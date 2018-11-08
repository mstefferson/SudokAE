import SudokuMaster
import numpy as np
import os


class PuzzelBuilder():
    def __init__(self, num_puzzels):
        self.main_dir = os.cwd()
        self.data_dir = main_dir + 'data/'
        self.puzzel_types = set(['solved', 'easy', 'moderate', 'hard'])
        self.solved_path = self.data_dir
        self.num_puzzels = num_puzzels
        self.puzzle_name = 'puzzle_{:0' + str(np.log10(num_puzzels)) + 'd}'

    def build_dir(self, dir_name):
        os.makedirs(dir_name, exists_ok=True)

    def build_data_dirs(self):
        self.build_dir(self.data_dir)
        for mdir in self.puzzel_types:
            mdir2build = self.main_dir + mdir + '/'
            self.build_dir(mdir2build + 'x')
            self.build_dir(mdir2build + 'y')

    def make_all_puzzels(self):
        for puzzel in self.puzzel_types:
            self.make_puzzle_data(puzzle)

    def make_puzzle_data(self, puzzle_type):
        dir2save = self.get_puzzle_dir(puzzle_type)
        for i in range(self.num_puzzles):
            save_name = dir2save + self.puzzle_name.format(i)
            p, b = make_puzzle_pair(puzzle_type)
            np.savetxt(dir2save + 'x', p)
            np.savetxt(dir2save + 'y', b)

    def make_puzzle_pair(self, puzzle_type):
        valid_puzzles = ['solved', 'easy', 'moderate', 'difficult']
        if puzzle_type not in valid_puzzles:
            raise ValueError('Unknown puzzle type, will break')
        # puzzle
        board = SudokuMaster.makeBoard()
        if puzzle_type == 'solved':
            puzzle = board
        else:
            puzzle = SudokuMaster.makePuzzleBoard(board, puzzle_type)
        return puzzle, board

    def get_puzzle_dir(self, puzzle_type):
        if puzzle_type not in valid_puzzles:
            raise ValueError('Unknown puzzle type, will break')
        return self.data_dir + puzzle_type + '/'

    def read_puzzles(self, puzzle_type):
        # Write me #
        dir2get = self.get_puzzle_dir(puzzle_type)


def build_logger(log_name='puzz_build'):
    # set-up logger
    logger = logging.getLogger('sat_build')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('sat_build.log', mode='w')
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
    puzz_builder = PuzzelBuilder(args.num_puzzles)
    logger.info('Initialized puzzle builder ')
    # build puzzle directories
    puzz_builder.build_data_dirs()
    logger.info('Built data directories')
    # build puzzles
    if args.puzzle == 'all':
        puzz_builder.make_all_puzzels()
    else:
        puzz_builder.make_all_puzzels()
    log_str = 'Building ' + args.puzzle + ' puzzles'
    logger.info(log_str)
    log_str = 'Built ' + args.num_puzzles + ' puzzles'
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
