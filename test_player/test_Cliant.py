from threading import Thread
import socket
import time

k = '\n'

class Cliant:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 4081
        self.buf_size = 1024
        self.keep_connect = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.keep_connact = True
        keep_connect_thread = Thread(target=self.keep_connect)
        keep_connect_thread.start()
        return

    def keep_connect(self):
        while self.keep_connect:
            self.send('')
            time.sleep(10)
        

    def send(self, message):
        if k not in message:
            message += k
        self.socket.send(message.encode('utf-8'))
        return

    def recv(self):
        message = self.socket.recv(self.buf_size).decode('utf-8')
        return str(message)

    def login(self, name, password):
        self.connect()
        self.send('LOGIN ' + name + ' ' + password)
        while True:
            message = self.recv()
            if 'LOGIN' in message:
                break
        if 'incorrect' in message:
            raise ValueError('LOGIN failed')
        return

    def logout(self):
        self.send('LOGOUT')
        self.keep_connect = False
        self.keep_connect_thread.join()
        self.socket.close()
        return

    def agree(self):
        self.send('AGREE')
        while True:
            m = self.recv()
            if 'START' in m:
                break
            if 'REJECT' in m:
                break
        return

    def wait(self):
        while True:
            message = self.recv()
            if 'Game_Summary' in message:
                break
        return self.Parse_summary(message)

    def Parse_summary(self, summary):
        #まだ
        lines = summary.splitlines()
        output = {'position': 'startpos moves', 'time': {'total': 0, 'inc': 0}, 'color': 0}
        for L in lines:
            if 'Your_Turn:' in L:
                if '+' in L:
                    output['color'] = 'black'
                else:
                    output['color'] = 'white'
            if 'Total_Time:' in L:
                output['time']['total'] = int(L[11:])
            if 'Increment:' in L:
                output['time']['inc'] = int(L[10:])
        return output

    def get_move(self):
        end = ['#ILLEGAL_MOVE', '#RESIGN', '#TIME_UP', '#DOUBLE_PASS', '#ABNORMAL', '#WIN', '#DRAW', '#LOSE']
        while True:
            m = self.recv()
            for e in end:
                if e in m:
                    m = 'end'
                    break
            if m == 'end':
                break
            if 'PASS' in m:
                m = 'pass'
                break
            if ',T' in m:
                m = m[1:3]
                break
        return m

    def send_move(self, usix_move, c):
        color = {'black': '+', 'white': '-'}[c]
        if usix_move == 'pass':
            self.send('PASS')
        else:
            self.send(color + usix_move)
        is_end = (self.get_move() == 'end')
        return is_end
