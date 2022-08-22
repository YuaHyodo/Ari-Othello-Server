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

def load_game(path):
    output = {'gamename': '', 'player': {}, 'moves': [], 'result': None}
    with open(path, 'r') as f:
        game = f.read()
    game = game.splitlines()
    read_moves = False
    for i in game:
        if 'Game_ID' in i:
            output['gamename'] = i.split(':')[1]
        if 'Name+' in i:
            output['player']['black'] = i.split(':')[1]
        if 'Name-' in i:
            output['player']['white'] = i.split(':')[1]
        if '%'  in i:
            output['result'] = [game[-2][1:], game[-1][1:], game[-3]]
            break
        if read_moves:
            if i == 'PASS':
                i = 'pass'
            output['moves'].append(i)
        if 'END Game_Summary' in i:
            read_moves = True
    return output
