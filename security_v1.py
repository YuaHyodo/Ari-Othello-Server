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

import hashlib
import json

username_available_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']

class Security:
    """
    セキュリティ関連の機能を追加する部分になる予定だが、
    その辺には疎いので全然追加されないと思う

    そもそも、あのfloodgateもパスワードを平文で流しているので、
    セキュリティとかそんなにいらないと思う。
    """
    def __init__(self, white_list_file='./Players/White_list.json'):
        self.white_list_file = white_list_file
        self.load_white_list()

    def load_white_list(self):
        #white "list"だが、型はdict
        with open(self.white_list_file, 'r') as f:
            self.white_list = json.load(f)
        return

    def return_digest(self, word):
        self.hash_algorithm = hashlib.md5()
        self.hash_algorithm.update(word.encode('utf-8'))
        return self.hash_algorithm.hexdigest()

    def login_check(self, username, password):
        """
        ログインしても良いならTrue, ダメならFalse
        """
        if False in [(i in username_available_characters) for i in ''.join(username.splitlines())] or len(username) > 30:
            return False
        if False in [(i in username_available_characters) for i in ''.join(password.splitlines())] or len(password) > 30:
            return False
        username = ''.join(username.split(' '))
        password = ''.join(password.split(' '))
        if username not in self.white_list.keys():
            #リストに名前なし
            return False
        if self.return_digest(password) != self.white_list[username]:
            #パスワードが違う
            return False
        return True

    def add_user(self, username, password):
        """
        ユーザーを追加する
        """
        self.white_list[username] = self.return_digest(password)
        with open(self.white_list_file, 'w') as f:
            json.dump(self.white_list, f)
        return

    def delete_user(self, username):
        self.white_list.pop(username)
        with open(self.white_list_file, 'w') as f:
            json.dump(self.white_list, f)
        return

if __name__ == '__main__':
    print('Ari-Othello-Server security_v1')
    S = Security()
    while True:
        command = input('command:')
        if command == 'add_user':
            S.add_user(input('username:'), input('password:'))
        if command == 'delete_user':
            S.delete_user(input('username:'))
        if command == 'print_white_list':
            print(S.white_list)
        if command == 'quit':
            break
