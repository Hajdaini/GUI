"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

import socket, threading, pickle, random, time


class Server:
    COLORS = ['red', 'hot pink', 'sienna', 'dark slate blue', 'forest green', 'maroon', 'SteelBlue4', 'SteelBlue3', 'DeepPink4']
    CLIENT_NUMBERS = 10
    IP = 'localhost'
    PORT = 22000

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((Server.IP, Server.PORT))
        self.server.listen(Server.CLIENT_NUMBERS)
        self.connections = []

    def handler(self, connection):
        while True:
            try:
                data = connection['client'].recv(1024)
            except:
                data = ''
            if not data:
                message_info = '[{}] {} ({}:{}) is disconnected'.format(time.strftime("%Y-%m-%d %H:%I:%S"),
                                                                     connection['username'], connection['info'][0],
                                                                     connection['info'][1])
                self.print_and_log(message_info)
                self.connections.remove(connection)
                connection['client'].close()
                break
            else:
                for conn in self.connections:
                    conn['client'].send(pickle.dumps({'username': connection['username'], 'data': data, 'color': connection['color']}))

    def print_and_log(self, message_info):
        print(message_info)
        with open('logs.txt', 'a') as file:
            file.write(message_info + '\n')

    def run(self):
        while True:
            client, info = self.server.accept()
            username = client.recv(1024).decode()
            connection = {'client': client, 'info': info, 'username': username, 'color': random.choice(Server.COLORS)}
            self.connections.append(connection)
            cThread = threading.Thread(target=self.handler, args=(connection, ))
            cThread.daemon = True
            cThread.start()
            message_info = '[{}] {} ({}:{}) is connected'.format(time.strftime("%Y-%m-%d %H:%I:%S"),connection['username'],  connection['info'][0], connection['info'][1])
            self.print_and_log(message_info)


server = Server()
server.run()
