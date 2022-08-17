"""
This file is part of Ari-Othello-Server

Copyright (c) 2022 YuaHyodo

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
"""

from test_Client import Client
from snail_reversi.Board import Board
import random
import time

class tester1(Client):
    def __init__(self):
        super().__init__()
        self.player_info = ['tester1', '1234']

    def main(self):
        self.login(self.player_info[0], self.player_info[1])
        summary = self.wait()
        print('ゲーム情報:', summary)
        self.agree()
        time.sleep(3)
        board = Board()
        a= False
        end = ['#ILLEGAL_MOVE', '#RESIGN', '#TIME_UP', '#DOUBLE_PASS', '#ABNORMAL']
        color = summary['color']
        if color == 'black':
            move = random.choice(board.gen_legal_moves())
            board.move_from_usix(move)
            print('自分の着手：', move)
            self.send_move(move, color)
        while True:
            print('')
            move = self.get_move()
            if move == 'end':
                break
            print('相手の着手:', move)
            board.move_from_usix(move)
            print('==============')
            print(board)
            print('is black turn:', board.turn)
            print('==============')
            move = random.choice(board.gen_legal_moves())
            board.move_from_usix(move)
            if self.send_move(move, color):
                break
            print('自分の着手：', move)
            print('')
        try:
            self.logout()
        except:
            pass
        return

if __name__ == '__main__':
    t = tester1()
    t.main()
    input('a;')
