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
from snail_reversi.Board import BLACK, WHITE, DRAW
from snail_reversi.Board import Board
from datetime import datetime
import read_gamefile
import os

HTML_file_list = []

def player_to_HTML(player):
    player_table = """
    <div id="Players_table_div">
    <table  id="Players_table"border="1" align="center">
    <caption>Player</caption>
    <thead>
    <tr>
    <th id="Black" bgcolor="black"><font color="white">Black</font></th>
    <th id="White" bgcolor="white"><font color="black">White</font></th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td headers="Black" bgcolor="Black" align="center"><font color="White">{}</font></td>
    <td headers="White" bgcolor="White" align="center"><font color="Black">{}</font></td>
    </tr>
    </tbody>
    </table>
    </div>
    """.format(player['black'], player['white'])
    return player_table

def moves_to_HTML_PD(moves):
    moves_html = """
    <select id="moves_PD" onchange="SetIndex(value)">
    <option value="0">startpos</option>
    """
    for i in range(len(moves)):
        moves_html += """<option value="{}">{}: {}</option>""".format(str(i+1), str(i+1), moves[i])
    moves_html += '</select>'
    return moves_html

def sfen_to_HTML_board(sfen, moves):
    ranks = [''] * 8
    colors = [[] for i in range(8)]
    for i in range(8):
        for j in range(8):
            colors[i].append(sfen[8 * i + j].replace('-', 'green').replace('X', 'black').replace('O', 'white'))
    fg = 'red'
    id_index = 0
    for i in range(1, 9):
        ranks[i - 1] = """
    <tbody>
    <tr align="center">
    <td headers="rank">{}</td>
    <td headers="a_file" bgcolor="{}" id="sq{}"><font color="{}">a{}</font></td>
    <td headers="b_file" bgcolor="{}" id="sq{}"><font color="{}">b{}</font></td>
    <td headers="c_file"  bgcolor="{}" id="sq{}"><font color="{}">c{}</font></td>
    <td headers="d_file" bgcolor="{}" id="sq{}"><font color="{}">d{}</font></td>
    <td headers="e_file" bgcolor="{}" id="sq{}"><font color="{}">e{}</font></td>
    <td headers="f_file" bgcolor="{}" id="sq{}"><font color="{}">f{}</font></td>
    <td headers="g_file" bgcolor="{}" id="sq{}"><font color="{}">g{}</font></td>
    <td headers="h_file" bgcolor="{}" id="sq{}"><font color="{}">h{}</font></td>
    </tr>
    """.format(i,
               colors[i - 1][0], id_index, fg, i,
               colors[i - 1][1], id_index + 1, fg, i,
               colors[i - 1][2], id_index + 2, fg, i,
               colors[i - 1][3], id_index + 3, fg, i,
               colors[i - 1][4], id_index + 4, fg, i,
               colors[i - 1][5], id_index + 5, fg, i,
               colors[i - 1][6], id_index + 6, fg, i,
               colors[i - 1][7], id_index + 7, fg, i)
        id_index += 8
    output = """
    <div id="HTML_Board_div">
    <table id="HTML_Board_table" border="1" bgcolor="green" align="center">
    <thead>
    <tr>
    <th id="rank" bgcolor="{}"> </th>
    <th id="a_file">a</th>
    <th id="b_file">b</th>
    <th id="c_file">c</th>
    <th id="d_file">d</th>
    <th id="e_file">e</th>
    <th id="f_file">f</th>
    <th id="g_file">g</th>
    <th id="h_file">h</th>
    </tr>
    </thead>
    """.format({'B': 'black', 'W': 'white'}[sfen[64]])
    for r in ranks:
        output += r
    output += """
    </tbody>
    </table>
    """
    output += """
    <table id="Stones_num_table" border="1" bgcolor="yellow" align="center">
    <thead>
    <tr>
    <th bgcolor="black" id="black_stone_num_show"><font color="white">Black: 2</font></th>
    <th bgcolor="white" id="white_stone_num_show"><font color="black">White: 2</font></th>
    </tr>
    </thead>
    </table>

    <table id="prev_and_next_button"  border="1" bgcolor="yellow" align="center">
    <thead>
    <tr>
    <th id="prev_button"><button onclick="Minus_index()">Prev</button></th>
    <th>{}</th>
    <th id="next_button"><button onclick="Plus_index()">Next</button></th>
    </tr>
    </thead>
    </table>
    </div>
    """.format(moves_to_HTML_PD(moves))
    return output

def moves_to_HTML(moves):
    moves_html = """
    <div id="moves_table_div">
    <table id="moves_table" border="1" bgcolor="green">
    <thead>
    <tr>
    <th id="move" align="center"><font color="yellow">moves</font></th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td headers="move"><button bgcolor="yellow" onclick="SetIndex(0)">startpos</button></td>
    """
    for i in range(len(moves)):
        moves_html += """<td headers="move"><button bgcolor="green" onclick="SetIndex({})">{}</button></td>""".format(str(i+1), moves[i])
    moves_html += '</tr></tbody></table></div>'
    return moves_html

def sfen_to_page(gamename, player, sfen, moves):
    output = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
    <meta charset="UTF-8">
    <title lang="en">{}</title>
    <script type="text/javascript" src="game_HTML_JS_v1.js"></script>
    <link href="game_CSS1.css" rel="stylesheet" type="text/css">
    </head>
    <body bgcolor="skyblue">
    <article>
    <div id="container">
    <p id="back_to_top"><a href="">top</a></p>
    """.format(gamename)
    for s in sfen:
        output += """<script>add_sfen("{}")</script>""".format(s)
    output += player_to_HTML(player)
    output += sfen_to_HTML_board(sfen[0], moves)
    #output += moves_to_HTML(moves)
    output += """
    </div>
    </article>
    </body>
    </html>
    """
    return output

def game_to_pages(data):
    link = './html/games/' + data['gamename'] + '.html'
    os.makedirs('./html/games/', exist_ok=True)
    board = Board()
    sfen_list = [board.return_sfen()]
    for i in range(len(data['moves'])):
        board.move_from_usix(data['moves'][i])
        sfen_list.append(board.return_sfen())
    html_txt = sfen_to_page(data['gamename'], data['player'], sfen_list, data['moves'])
    with open(link, 'w') as f:
        f.write(html_txt)
    return

def update_recent_games_list(game_list):
    file = './html/recent_games_list.html'
    output = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
    <meta charset="UTF-8">
    <title lang="ja"> サイトの名前 Games</title>
    </head>
    <body bgcolor="skyblue">
    <article>
    <p><a href="">top</a></p>
    <table border="1" bgcolor="yellow" align="center" width="700px">
    <caption>Games</caption>
    <thead>
    <tr>
    <th id="time" width="150px" height="10px"><font color="green">time</font></th>
    <th id="link" width="550px" height="10px"><font color="red">link</font></th>
    </tr>
    </thead>
    <tbody>
    """
    for game in game_list:
        link = './games/' + game.ID + '.html'
        output += """
        <tr align="center">
        <td headers="time" width=150px">{}</td>
        <td headers="link" width="550px"><a href="{}">{}</a></td>
        </tr>
        """.format(str(datetime.now()), link, game.ID)
    
    oldgames = os.listdir('./games/')
    for i in range(len(oldgames)):
        if '.txt' not in oldgames[i]:
            continue
        gameID = oldgames[i].split('.')[0]
        link = './games/' + gameID + '.html'
        output +="""
        <tr align="center">
        <td headers="time" width="150px">{}</td>
        <td headers="link" width="550px"><a href="{}">{}</a></td>
        </tr>
        """.format('?(old)', link, gameID)
    output += """</tbody></table></article></body></html>"""
    with open(file, 'w') as f:
        f.write(output)
    return

def main():
    files = os.listdir('./games/')
    for i in range(len(files)):
        if '.txt' in files[i]:
            data = read_gamefile.load_game('./games/' + files[i])
            game_to_pages(data)
            HTML_file_list.append(files[i])
    return

if __name__ == '__main__':
    update_recent_games_list([])
    main()
