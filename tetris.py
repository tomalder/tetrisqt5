# -*- config: utf-8 -*-

import sys
import random
import math
import numpy as np
from block import Block


class Stage(object):
    def __init__(self):
        self.field = (10 + 2, 20 + 2)
        self.board = np.zeros((self.field[1], self.field[0]))
        self.generate_wall()
        self.bl = Block()
        self.moving_block = np.zeros((4, 4))
        self.next_block = np.zeros((4, 4))

        self.position = []
        self.rotation = 0
        self.init_posture()

        self.fixed_board = []
        self.save_board()
        self.past_board = []
        self.flag_move = False
        self.over = False

    def init_posture(self):
        '''
        ブロックは4x4のリストで表現されている
        実際にブロックがあるのはそのリストの２行目からなので
        ｙの初期位置を-2に
        '''
        self.position = np.array([4, -2])
        self.rotation = 0

    def generate_wall(self):
        for col in range(self.field[0]):
            self.board[self.field[1] - 1][col] = -1
            if col <= 3 or col >= 8:
                self.board[0][col] = -1
        for row in range(self.field[1]):
            self.board[row][self.field[0] - 1] = -1
            self.board[row][0] = -1

    def select_block(self, block_num):
        return np.array(self.bl.list[block_num])

    def save_board(self):
        self.fixed_board = np.array(self.board)

    def update_block(self):
        self.past_board = np.array(self.board)
        self.board = np.array(self.fixed_board)

        x = self.position[0]
        y = self.position[1]
        for col in range(4):
            for row in range(4):
                if self.moving_block[row][col] != 0:
                    self.board[y + row][x + col] = self.moving_block[row][col]

    def clear_block(self, x, y):
        for col in range(4):
            for row in range(4):
                self.board[y + row][x + col] = 0

    def rotate(self, block, rotation):
        for count in range(rotation):
            block = np.copy(self.bl.rotation(block))
        return block

    def move_block(self, x, y):
        self.position = [x, y]
        self.update_block()

    def check_movable(self, block, position, next_x=0, next_y=0, next_rot=0):
        x = position[0] + next_x
        y = position[1] + next_y
        tmp_block = self.rotate(block, next_rot)
        for col in range(4):
            for row in range(4):
                if tmp_block[row][col] != 0 and \
                   self.fixed_board[y + row][x + col] != 0:
                    return False
        return True

    def check_rotatable(self):
        block = np.array(self.bl.rotation(self.moving_block))
        return self.check_movable(block, self.position, 0, 0)

    def get_moving_block_num(self):
        num = self.moving_block[self.moving_block != 0][0]
        return int(num)

    def remove_lined_blocks(self):
        for row in range(1, self.field[1]-1):
            line = self.fixed_board[row][:]
            if np.count_nonzero(line) == self.field[0]:
                self.fixed_board = np.delete(self.fixed_board, row, 0)
                self.fixed_board = np.insert(self.fixed_board, 1, 0, 0)
                self.fixed_board[1][0] = self.fixed_board[1][-1] = -1

    def judge_gameover(self):
        line = self.fixed_board[1][4:-4]
        if np.count_nonzero(line) > 0 and self.position[1] == -2:
            return True
        return False


def main():

    st = Stage()
    st.moving_block = st.select_block(5)

    st.move_block(4, 0)
    print(st.board)

    st.rotate(st.moving_block, 1)
    print(st.moving_block)

    st.move_block(4, 1)
    print(st.board)

    if st.check_movable(st.moving_block, st.position, -4, 0) is True:
        print('can move the block')
    else:
        print('cannot move the block')

    if st.check_rotatable() is True:
        print('can rotate the block')
    else:
        print('cannot rotate the block')

    st.remove_lined_blocks()
    print(st.board)

    st.judge_gameover()

if __name__ == '__main__':

    main()
