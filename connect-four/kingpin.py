#! /usr/bin/python

import sys
import time
import thread
import player
import signal

range1 = [3,2,4,1,5,0,6]
p0wins = 100000000
p1wins = -100000000
null_win = [None for i in range(4)]

global val

def call_it(game, depth, p1wins, p0wins, player_is_zero, heuristic):
    val = player.call_alphabeta(game, depth, p1wins, p0wins, player_is_zero, heuristic)

def _handle_timeout(signum, frame):
    raise Exception()

def kingpin():
    game = player.OldGame()
    player_is_zero = False
    movenum = 0

    while not sys.stdin.closed:
        line = sys.stdin.readline()
        if line == 'go!\n':
            player_is_zero = True
        else:
            game.push_move(line)
            movenum += 1

        valid = game.valid_moves
        bestmove = valid[0]
        depth = 1
        signal.signal(signal.SIGALRM, _handle_timeout)
        signal.setitimer(signal.ITIMER_REAL,0.95)
        # bestmove = player.call_alphabeta(game, depth, p1wins, p0wins, player_is_zero, player.potential(10))
        moves = valid
        while True:
            try:
                trash('Depth: %s' % depth)
                moves = player.call_alphabeta(game, depth, p1wins, p0wins, player_is_zero, player.potential(10), moves)
                # trash(move)
                move = moves[0]
                bestmove = move if move in valid else valid[0]
                trash(bestmove)
                depth += 1
                # game.print_grid()
            except:
                break
        print(bestmove)

        while len(game.moves) > movenum:
            game.pull_move()

        game.push_move(bestmove)
        movenum += 1
        game.print_grid()

        sys.stdout.flush()


def trash(str_):
    sys.stderr.write("%s\n" % str_)

if __name__ == '__main__':
    # while not sys.stdin.closed:
    #     line = sys.stdin.readline()
    #     print(1)
    #     sys.stdout.flush()
    kingpin()
