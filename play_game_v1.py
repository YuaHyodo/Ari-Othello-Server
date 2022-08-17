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

"""
メッセージをlistに格納して、それを順番に送るようにすると
まだマシになりそうなので、あとでやる。
"""
from snail_reversi.Board import Board
import time

from rate_v1 import update_rate
#改行を表す
k = '\n'

class game:
    def __init__(self, player1, player2, time_setting={'total': 300, 'inc': 10}):
        self.player1 = player1#先手
        self.player2 = player2#後手
        self.time_setting = time_setting#時間設定
        self.ID = 'game-' + player1.name + '-VS-' +player2.name + '-' + str(time.time()).replace('.', '')#ゲームID
        self.file_name = './games/' + self.ID + '.txt'#保存先ファイル名
        self.file_text = ''#ファイルに書き込む文章

    def write(self):#ファイルに書き込む
        with open(self.file_name, 'w') as f:
            f.write(self.file_text)
        return

    def start(self):#startという名前だが、これで完結している
        #ゲームサマリー(ゲームの情報に関するメッセージ)を各プレーヤに送信
        self.send_gamesummary(player_color='+')
        self.send_gamesummary(player_color='-')
        agree = [False, False]
        #返事待ち
        while True:
            m = self.player1.recv_message()
            if 'AGREE' in m:
                agree[0] = True
                break
            if 'REJECT' in m:
                break
        while True:
            m = self.player2.recv_message()
            if 'AGREE' in m:
                agree[1] = True
                break
            if 'REJECT' in m:
                break
        #両方agreeしたか？
        if agree[0] and agree[1]:
            #したのでスタート
            self.player1.send_message('START' + k)
            self.player2.send_message('START' + k)
        else:
            #どちらかが拒否したので停止
            if not agree[0]:
                r_name = self.player1.name
            else:
                r_name = self.player2.name
            self.player1.send_message('REJECT' + k)
            self.player2.send_message('REJECT' + k)
            return 'REJECT'
        #開始
        self.main_loop()
        return

    def send_gamesummary(self, player_color='+'):
        summary = 'BEGIN Game_Summary'
        summary += k
        summary += 'Protocol_Version: 0.0.1'
        summary += k
        summary += ('Game_ID:' + self.ID)
        summary += k
        summary += ('Name+:' + self.player1.name)
        summary += k
        summary += ('Name-:' + self.player2.name)
        summary += k
        summary += ('Your_Turn:' + player_color)
        summary += k
        summary += 'To_Move:+'
        summary += k
        summary += 'BEGIN Time'
        summary += k
        summary += ('Total_Time:' + str(self.time_setting['total']))
        summary += k
        summary += ('Increment:' + str(self.time_setting['inc']))
        summary += k
        summary += 'END Time'
        summary += k
        summary += 'BEGIN Position'
        summary += k
        summary += 'position startpos'
        summary += k
        summary += 'END Position'
        summary += k
        summary += 'END Game_Summary'
        summary += k
        if player_color == '+':
            self.player1.send_message(summary)
        else:
            self.player2.send_message(summary)
        self.file_text += summary
        return

    def return_winner(self, board):
        my = board.piece_num()
        opponent = board.opponent_piece_num()
        if my == opponent:
            return 'draw'
        if my > opponent:
            if board.turn:
                return 'black'
            return 'white'
        if board.turn:
            return 'white'
        return 'black'

    def main_loop(self):
        #メインループ(不完全)
        #合法手チェック用
        board = Board()
        #残りの持ち時間
        player1_time = self.time_setting['total']
        player2_time = self.time_setting['total']
        #色々
        result = [None, None]
        moves_list = []
        while True:
            #先手の行動
            move, t = self.player1.get_move(player1_time + self.time_setting['inc'])
            #時間などの管理
            player1_time -= t
            player1_time += self.time_setting['inc']
            #時間が切れたか？
            if player1_time <= 0:
                self.player1.send_message('#TIME_UP')
                self.player2.send_message('#TIME_UP')
                self.player1.send_message('#LOSE')
                self.player2.send_message('#WIN')
                self.file_text += ('%TIME_UP' + k)
                result = ['lose', 'win']
                break
            #投了したか？
            if move == 'RESIGN':
                self.player1.send_message('#RESIGN')
                self.player2.send_message('#RESIGN')
                self.player1.send_message('#LOSE')
                self.player2.send_message('#WIN')
                self.file_text += ('%TORYO' + k)
                result = ['lose', 'win']
                break
            #手番を変更
            message = move + ',T' + str(t)
            self.player1.send_message('+' + message)
            self.player2.send_message('+' + message)
            if 'PASS' in move:
                usix_move = 'pass'
            else:
                usix_move = move
            if usix_move not in board.gen_legal_moves():
                self.player1.send_message('#ILLEGAL_MOVE')
                self.player2.send_message('#ILLEGAL_MOVE')
                self.player1.send_message('#LOSE')
                self.player2.send_message('#WIN')
                self.file_text += ('%ILLEGAL_MOVE' + k)
                self.file_text += ("'illegal_move: " + usix_move + k)
                self.file_text += ("'legal_moves: " + str(board.gen_legal_moves()) + k)
                result = ['lose', 'win']
                break
            board.move_from_usix(usix_move)
            moves_list.append(move)
            self.file_text += (move + k)
            if board.is_gameover() or (len(moves_list) >= 2 and moves_list[-1] == moves_list[-2]):
                winner = self.return_winner(board)
                self.player1.send_message('#DOUBLE_PASS')
                self.player2.send_message('#DOUBLE_PASS')
                if winner == 'draw':
                    self.player1.send_message('#DRAW')
                    self.player2.send_message('#DRAW')
                    result = ['draw', 'draw']
                if winner == 'black':
                    self.player1.send_message('#WIN')
                    self.player2.send_message('#LOSE')
                    result = ['win', 'lose']
                if winner == 'white':
                    self.player1.send_message('#LOSE')
                    self.player2.send_message('#WIN')
                    result = ['lose', 'win']
                self.file_text += ('%DOUBLE_PASS' + k)
                break
            
            #後手番
            move, t = self.player2.get_move(player2_time + self.time_setting['inc'])
            player2_time -= t
            player2_time += self.time_setting['inc']
            if player2_time <= 0:
                self.player2.send_message('#TIME_UP')
                self.player1.send_message('#TIME_UP')
                self.player2.send_message('#LOSE')
                self.player1.send_message('#WIN')
                self.file_text += ('%TIME_UP' + k)
                result = ['win', 'lose']
                break
            if move == 'RESIGN':
                self.player2.send_message('#RESIGN')
                self.player1.send_message('#RESIGN')
                self.player2.send_message('#LOSE')
                self.player1.send_message('#WIN')
                self.file_text += ('%TORYO' + k)
                result = ['win', 'lose']
                break
            message = move + ',T' + str(t)
            self.player2.send_message('-' + message)
            self.player1.send_message('-' + message)
            if 'PASS' in move:
                usix_move = 'pass'
            else:
                usix_move = move
            if usix_move not in board.gen_legal_moves():
                self.player2.send_message('#ILLEGAL_MOVE')
                self.player1.send_message('#ILLEGAL_MOVE')
                self.player2.send_message('#LOSE')
                self.player1.send_message('#WIN')
                self.file_text += ('%ILLEGAL_MOVE' + k)
                self.file_text += ("'illegal_move: " + usix_move + k)
                self.file_text += ("'legal_moves: " + str(board.gen_legal_moves()) + k)
                result = ['win', 'lose']
                break
            board.move_from_usix(usix_move)
            moves_list.append(move)
            self.file_text += (move + k)
            if board.is_gameover() or (len(moves_list) >= 2 and moves_list[-1] == moves_list[-2]):
                winner = self.return_winner(board)
                self.player1.send_message('#DOUBLE_PASS')
                self.player2.send_message('#DOUBLE_PASS')
                if winner == 'draw':
                    self.player1.send_message('#DRAW')
                    self.player2.send_message('#DRAW')
                    result = ['draw', 'draw']
                if winner == 'black':
                    self.player1.send_message('#WIN')
                    self.player2.send_message('#LOSE')
                    result = ['win', 'lose']
                if winner == 'white':
                    self.player1.send_message('#LOSE')
                    self.player2.send_message('#WIN')
                    result = ['lose', 'win']
                self.file_text += ('%DOUBLE_PASS' + k)
                break
        #棋譜を保存
        self.write()
        #リザルトを反映
        self.player1.update_player_data(result[0])
        self.player2.update_player_data(result[1])
        d = {'win': 1, 'draw': 0.5, 'lose': 0}
        r = [d[result[0]], d[result[1]]]
        rate1, rate2 = update_rate(r, self.player1.player_data['rate'], self.player2.player_data['rate'])
        self.player1.player_data['rate'] = rate1
        self.player2.player_data['rate'] = rate2
        self.player1.write_player_data()
        self.player2.write_player_data()
        return

    
