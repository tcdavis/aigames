#! /usr/bin/python

import sys
import time
from copy import deepcopy as copy

range1 = [3,2,4,1,5,0,6]
p0wins = 100000000
p1wins = -100000000

null_win = [None for i in range(4)]

import operator as op
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

_row=0
_col=1
_left=2
_right=3



#(index, startpos)
def get_row(move):
    (c,r) = move
    return r, c

def get_col(move):
    (c,r) = move
    return c, r

def get_left(move):
    (c,r) = move
    return r-c, min(r,c)

def get_right(move):
    (c,r) = move
    return c+r, min(c,6-r)


class Game(object):

    ROWS = 6
    COLUMNS = 7

    def __init__(self):
        self.moves = []
        self.next = [0 for i in range(self.COLUMNS)]
        self.wins = {
            _row: {j: [null_win for i in range(self.COLUMNS - 3)] for j in self.ROWS},
            _col: {j: [null_win for i in range(self.ROWS - 3)] for j in self.COLUMNS},
            _left: {j+3: [null_win for i in range(min(j, 6 - j)+1)] for j in range(6)},
            _right: {j-2: [null_win for i in range(min(j, 6 - j)+1)] for j in range(6)}
            }

    def expand(self, move):
        return (move, self.next[move])

    @property
    def p0toMove(self):
        return not bool(len(self.moves) % 2)

    def push_move(self, move):
        move = int(move)
        # insert move into grid_columns
        for row_idx, cell in enumerate(self.grid_columns[col_idx]):
            if cell is None:
                self.grid_columns[col_idx][row_idx] = len(self.moves) % 2
                break
        else:
            raise ValueError('invalid move! column %s is full.' % col_idx)
        # insert move into grid_rows
        self.grid_rows[row_idx][col_idx] = len(self.moves) % 2
        self.moves.append(col_idx)
        return self

    @property
    def valid_moves(self):
        # print 'top:', self.grid_rows[5]
        valid =  [i for i in range1 if self.grid_rows[5][i] is None]
        # print 'valid', valid
        return valid

    def print_grid(self):
        trash('-' * (Game.COLUMNS * 2 + 3))
        for row in self.grid_rows[::-1]:
            trash('| %s |' % ' '.join([str(cell if cell is not None else ' ') for cell in row]))
        trash('-' * (Game.COLUMNS * 2 + 3))

    def is_won(self):
        # _ = self.grid_rows + self.grid_columns + self.diags
        # for line in _:
        #     if len(line) < 4:
        #         continue
        #     zeros = [1 if cell == 0 else 0 for cell in line]
        #     ones = [1 if cell == 1 else 0 for cell in line]

        #     zeros = map(lambda *args: sum(args), *[zeros[i:itersafe(-4 + i)] for i in range(4)])
        #     ones = map(lambda *args: sum(args), *[ones[i:itersafe(-4 + i)] for i in range(4)])


        #     for i in range(len(zeros)):
        #         if zeros[i] == 4 or ones[i] == 4:
        #             return True
        # return False
        return (self.any_columns_won() or self.any_rows_won() or
            self.any_diags_won())

    def is_full(self):
        return len(self.moves) == Game.ROWS * Game.COLUMNS

    def any_columns_won(self):
        return any(self.check_series(column) for column in self.grid_columns)

    def any_rows_won(self):
        return any(self.check_series(row) for row in self.grid_rows)

    def any_diags_won(self):
        return any(self.check_series(diag) for diag in self.diags)

    def check_series(self, series):
        if len(series) < 4:
            return False
        for idx in xrange(0, len(series) - 3):
            if ([series[idx]] * 4 == series[idx:idx + 4] and
                    all((x is not None for x in series[idx:idx + 4]))):
                return True
        return False

    @property
    def diags(self):
        def get_diags(right=True):
            # val = [
            #     [(c, c + delta if right else c - delta,delta)
            #         for delta in xrange(min(c if not right else Game.COLUMNS-1-c, Game.ROWS-1))]
            #     for c in xrange(Game.COLUMNS)]
            # trash(val)
            # return [[self.grid_columns[r][c] for (d,r,c) in set_] for set_ in val] 
            return [
                [self.grid_rows[r + delta][c + (delta if right else -delta)]
                    for delta in xrange(min(Game.ROWS - r, (Game.COLUMNS - c if right else c)))]
                for r in xrange(Game.ROWS)
                for c in xrange(Game.COLUMNS)]
        return get_diags(right=True) + get_diags(right=False)


class OldGame(object):

    ROWS = 6
    COLUMNS = 7

    def __init__(self):
        self.moves = []
        self.grid_columns = [[None for _ in xrange(Game.ROWS)] for _ in xrange(Game.COLUMNS)]
        self.grid_rows = [[None for _ in xrange(Game.COLUMNS)] for _ in xrange(Game.ROWS)]

    @property
    def p0toMove(self):
        return not bool(len(self.moves) % 2)

    def push_move(self, move):
        col_idx = int(move)
        # insert move into grid_columns
        for row_idx, cell in enumerate(self.grid_columns[col_idx]):
            if cell is None:
                self.grid_columns[col_idx][row_idx] = len(self.moves) % 2
                break
        else:
            raise ValueError('invalid move! column %s is full.' % col_idx)
        # insert move into grid_rows
        self.grid_rows[row_idx][col_idx] = len(self.moves) % 2
        self.moves.append(col_idx)
        return self

    def pull_move(self):
        col_idx = self.moves.pop()
        # insert move into grid_columns
        for row_idx, cell in enumerate(reversed(self.grid_columns[col_idx])):
            if cell is not None:
                row_idx = self.ROWS -1 - row_idx
                self.grid_columns[col_idx][row_idx] = None
                break
        else:
            raise ValueError('Wierd!')
       # insert move into grid_rows
        self.grid_rows[row_idx][col_idx] = None
        return self

    @property
    def valid_moves(self):
        # print 'top:', self.grid_rows[5]
        valid =  [i for i in range1 if self.grid_rows[5][i] is None]
        # print 'valid', valid
        return valid

    def print_grid(self):
        trash('-' * (Game.COLUMNS * 2 + 3))
        for row in self.grid_rows[::-1]:
            trash('| %s |' % ' '.join([str(cell if cell is not None else ' ') for cell in row]))
        trash('-' * (Game.COLUMNS * 2 + 3))

    def is_won(self):
        # _ = self.grid_rows + self.grid_columns + self.diags
        # for line in _:
        #     if len(line) < 4:
        #         continue
        #     zeros = [1 if cell == 0 else 0 for cell in line]
        #     ones = [1 if cell == 1 else 0 for cell in line]

        #     zeros = map(lambda *args: sum(args), *[zeros[i:itersafe(-4 + i)] for i in range(4)])
        #     ones = map(lambda *args: sum(args), *[ones[i:itersafe(-4 + i)] for i in range(4)])


        #     for i in range(len(zeros)):
        #         if zeros[i] == 4 or ones[i] == 4:
        #             return True
        # return False
        return (self.any_columns_won() or self.any_rows_won() or
            self.any_diags_won())

    def is_full(self):
        return len(self.moves) == Game.ROWS * Game.COLUMNS

    def any_columns_won(self):
        return any(self.check_series(column) for column in self.grid_columns)

    def any_rows_won(self):
        return any(self.check_series(row) for row in self.grid_rows)

    def any_diags_won(self):
        return any(self.check_series(diag) for diag in self.diags)

    def check_series(self, series):
        if len(series) < 4:
            return False
        for idx in xrange(0, len(series) - 3):
            if ([series[idx]] * 4 == series[idx:idx + 4] and
                    all((x is not None for x in series[idx:idx + 4]))):
                return True
        return False

    @property
    def diags(self):
        def get_diags(right=True):
            # val = [
            #     [(c, c + delta if right else c - delta,delta)
            #         for delta in xrange(min(c if not right else Game.COLUMNS-1-c, Game.ROWS-1))]
            #     for c in xrange(Game.COLUMNS)]
            # trash(val)
            # return [[self.grid_columns[r][c] for (d,r,c) in set_] for set_ in val] 
            return [
                [self.grid_rows[r + delta][c + (delta if right else -delta)]
                    for delta in xrange(min(Game.ROWS - r, (Game.COLUMNS - c if right else c)))]
                for r in xrange(Game.ROWS)
                for c in xrange(Game.COLUMNS)]
        return get_diags(right=True) + get_diags(right=False)


def alphabeta(game, depth, a, b, player_is_zero, heuristic):
    if game.is_won():
        # trash('won')
        return p1wins if game.p0toMove else p0wins
    if depth == 0:
        return heuristic(game)
    if player_is_zero:
        for i in game.valid_moves:
            result = alphabeta(game.push_move(i), depth - 1, a, b, False, heuristic)
            game.pull_move()
            a = max([a, result])
            if b <= a:
                break
        return a
    else:
        for i in game.valid_moves:
            result = alphabeta(game.push_move(i), depth - 1, a, b, True, heuristic)
            game.pull_move()
            b = min([b, result])
            if b <= a:
                break

        return b


def call_alphabeta(game, depth, a, b, player_is_zero, heuristic, moves=None):
    if moves is None:
        moves = game.valid_moves
    move_val = [0 for i in range(7)]
    bestmove = 1
    if player_is_zero:
        for i in moves:
            result = alphabeta(game.push_move(i), depth - 1, a, b, False, heuristic)
            game.pull_move()
            move_val[i] = -result
            if result > a:
                a = result
                bestmove = i
            if b <= a:
                break

    else:
        for i in moves:
            result = alphabeta(game.push_move(i), depth - 1, a, b, True, heuristic)
            game.pull_move()
            move_val[i] = result
            if result < b:
                b = result
                bestmove = i
            if b <= a:
                break

    # printi(move_val)
    # game.print_grid()

    trash(moves)
    trash(move_val)
    final = [move for (val, move) in sorted(zip(move_val, range(7))) if move in game.valid_moves]
    trash(final)
    return final



def detect_win(heuristic):
    def new_h(board):
        if board.is_won():
            # printi('oh look')
            return p1wins if board.p0toMove else p0wins
        else:
            return heuristic(board)
    return new_h

def itersafe(n):
    return n if n else None

@detect_win
def simple(board):
    # board.print_grid()
    # print board.valid_moves
    score = 0
    _ = board.grid_columns
    for val, line in enumerate(_):
        s = (map(lambda x: val if x==0 else 0, line) + 
             map(lambda x: -val if x==1 else 0, line))
        if s:
            # print line, s, sum(s)
            score += (sum(s))
    return score


def potential(base):
    def h(board):
        score = 0
        _ = board.grid_rows + board.grid_columns + board.diags
        for line in _:
            if len(line) < 4:
                continue
            zeros = [1 if cell == 0 else 0 for cell in line]
            ones = [1 if cell == 1 else 0 for cell in line]

            zeros = map(lambda *args: sum(args), *[zeros[i:itersafe(-4 + i)] for i in range(4)])
            ones = map(lambda *args: sum(args), *[ones[i:itersafe(-4 + i)] for i in range(4)])


            for i in range(len(zeros)):
                score += pow(base,zeros[i]) if not ones[i] else 0
                score -= pow(base,ones[i]) if not zeros[i] else 0

        return score
    return h

def player(depth, heuristic):
    game = OldGame()
    player_is_zero = False
    while not sys.stdin.closed:
        line = sys.stdin.readline()
        if line == 'go!\n':
            player_is_zero = True
        else:
            game.push_move(line)
        move = call_alphabeta(game, depth, p1wins, p0wins, player_is_zero, heuristic)
        valid = game.valid_moves
        if valid:
            if move not in valid:
                move = valid[0]
            print(move)
            game.push_move(move)
            # game.print_grid()
            sys.stdout.flush()
        else:
            trash("The games over, dude")
            trash("Here, look")
            game.print_grid()
            time.sleep(5)
            trash("Fine, but I should get a point")
            time.sleep(1)
            print("This is bullshit")
            sys.stdout.flush()


def trash(str_):
    sys.stderr.write("%s\n" % str_)

if __name__ == '__main__':
    # while not sys.stdin.closed:
    #     line = sys.stdin.readline()
    #     print(1)
    #     sys.stdout.flush()
    player(5, potential(10))
