from test_Cliant import Cliant
from snail_reversi.Board import Board
import random
import time

class tester1(Cliant):
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
