"""
Knight's Tour

Given a starting square, output a sequence of moves that will bring a knight
from that square to every square on the board.

One-line unit test in bash:

  for i in {0..7}; do for j in {0..7}; do python knight_tour.py --start $i,$j; done; done;

Paul Bissex <paul@bissex.net> December 2015
"""
import argparse
import os
import random
import sys
import time


class Board(object):

    ALL_KNIGHT_MOVES = [(-2, -1), (-2, 1), (2, -1), (2, 1),
                        (-1, -2), (-1, 2), (1, -2), (1, 2)]
    EMPTY, VISITED, KNIGHT = ".", "o", "K"

    @staticmethod
    def in_bounds(x, y):
        return (0 <= x <= 7 and 0 <= y <= 7)

    def __init__(self, start):
        self.board = [[self.EMPTY for col in range(8)] for row in range(8)]
        self.knight = start
        self.move(*start)

    def move(self, x, y):
        self.board[self.knight[1]][self.knight[0]] = self.VISITED
        self.board[y][x] = self.KNIGHT
        self.knight = (x, y)

    def free(self, x, y):
        return self.board[y][x] == self.EMPTY

    def complete(self):
        return not any(self.EMPTY in row for row in self.board)

    def possible_moves(self, x=None, y=None):
        if x is None and y is None:
            x, y = self.knight
        moves = []
        for delta_x, delta_y in self.ALL_KNIGHT_MOVES:
            new_x = x + delta_x
            new_y = y + delta_y
            if self.in_bounds(new_x, new_y) and self.free(new_x, new_y):
                moves.append((new_x, new_y))
        return moves

    def warnsdorff_pick(self):
        # See https://en.wikipedia.org/wiki/Knight%27s_tour#Warnsdorff.27s_rule
        moves = self.possible_moves()
        graded_squares = {}
        for x, y in moves:
            graded_squares[(x, y)] = len(self.possible_moves(x, y))
        return min(graded_squares, key=graded_squares.get)

    def tour(self, animate=False):
        moves = [self.knight]
        while not self.complete():
            move = self.warnsdorff_pick()
            self.move(*move)
            moves.append(move)
            if animate:
                os.system("clear")
                print board
                time.sleep(.5)
        return moves

    def __str__(self):
        rows = [" ".join(row) for row in self.board]
        return "\n".join(rows) + "\n"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Solve the Knight's Tour problem")
    parser.add_argument("--animate", action="store_true", help="Show each move")
    parser.add_argument("--start", default="1,7", help="Starting location X,Y from upper left")
    args = parser.parse_args()

    start = map(int, args.start.split(","))
    board = Board(start=start)
    print board
    moves = board.tour(animate=args.animate)
    print "Solved.\n{}\nMoves: {}".format(board, moves)
