"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

import socket, threading, pickle
from gui import Gui


class Client:
    IP = 'localhost'
    PORT = 22000

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ''
        self.gui = []
        self.is_connected = False

    def window_input_for_username(self):
        self.gui = Gui(self)
        self.gui.window_config()
        self.gui.widget_for_username()
        self.gui.window.mainloop()

    def connection(self):
        try:
            self.client.connect((Client.IP, Client.PORT))
            self.is_connected = True
            return True
        except:
            return False

    def send_username_to_server(self):
        self.client.send(self.username.encode())

    def thread_chatbox_gui_creation(self):
        tk_thread = threading.Thread(target=self.gui.window_creation)
        tk_thread.daemon = True
        tk_thread.start()

    def close(self):
        try:
            self.client.close()
        except:
            print('no socket to close')

    def data_recv_handle(self):
        return_value = True
        try:
            data = pickle.loads(self.client.recv(1024))
        except:
            data = ''
        if not data:
            return_value = False
        else:
            self.gui.display_msg_in_chatbox(data['username'], data['data'].decode(), data['color'])

        return return_value

    def run(self):
        self.window_input_for_username()

        if not self.is_connected:
            return None

        self.send_username_to_server()
        self.thread_chatbox_gui_creation()

        while True:
            if not self.data_recv_handle():
                break


client = Client()
client.run()
client.close()
print('Good bye ' + client.username)
