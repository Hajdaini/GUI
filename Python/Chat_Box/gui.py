from tkinter import *

class Gui:
    WINDOW_HEIGHT = 500
    WINDOW_WIDTH = 400
    BG_COLOR = "#011627"
    
    def __init__(self, client_instance):
        self.client_instance = client_instance
        self.windows_init()
        self.window_input_for_username_init()

    def windows_init(self):
        self.window = []
        self.entry_box = []
        self.chat_log = []
        self.scrollbar = []
        self.send_button = []

    def window_input_for_username_init(self):
        self.input_username = []
        self.label_error = []

    def display_msg_in_chatbox(self, username, message, color):
        username_len_tag = len(username) / 10
        if message != '':
            self.chat_log.config(state=NORMAL)
            if self.chat_log.index('end') != None:
                LineNumber = float(self.chat_log.index('end')) - 1.0
                self.chat_log.insert(END, username + ": " + message)
                self.chat_log.tag_add(username, LineNumber, LineNumber + username_len_tag)
                self.chat_log.tag_config(username, foreground=color,  font=("Arial", 10, "bold"))
                self.chat_log.config(state=DISABLED)
                self.chat_log.yview(END)

    def window_creation(self):
        self.window_config()
        self.window_add_widgets()
        self.window_widgets_place()
        self.window.mainloop()

    def window_config(self):
        self.window = Tk()
        self.window.title('Hajdaini chat')
        self.window_position()
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.configure(bg=Gui.BG_COLOR)

    def window_position(self):
        screen_width = int(self.window.winfo_screenwidth())
        screen_height = int(self.window.winfo_screenheight())
        window_width = Gui.WINDOW_WIDTH
        window_height = Gui.WINDOW_HEIGHT
        window_x = (screen_width // 2) - (window_width // 2)
        window_y = (screen_height // 2) - (window_height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(window_width, window_height, window_x, window_y))

    def window_widgets_place(self):
        self.scrollbar.place(x=376, y=6, height=386)
        self.chat_log.place(x=6, y=6, height=386, width=370)
        self.entry_box.place(x=6, y=401, height=90, width=265)
        self.chat_log.insert(END, "You: " + 'test')
        self.send_button.place(x=278, y=401, height=90)

    def window_add_widgets(self):
        self.chat_log = Text(self.window, bd=0, bg="white", height="8", width="50", font="Arial 10 normal italic", )
        self.chat_log.insert(END, "Welcome to Hajdaini chat..\n")
        self.chat_log.config(state=DISABLED)
        self.scrollbar = Scrollbar(self.window, command=self.chat_log.yview, cursor="heart")
        self.chat_log['yscrollcommand'] = self.scrollbar.set
        self.entry_box = Text(self.window, bd=0, bg="white", width="29", height="5", font="Arial 10 normal")
        self.send_button = Button(self.window, font="Arial 12 bold", text="Send", width="11", height=5,
                                 bd=0, bg="#F71735", fg='RosyBrown2', activebackground="#a51327",
                                 activeforeground='RosyBrown2', command=self.send_button_click_event)

    def send_button_click_event(self):
        message = self.entry_box.get("0.0", END)
        self.client_instance.client.send(message.encode())
        self.entry_box.delete("0.0", END)

    def on_closing(self):
        self.window.quit()
        self.client_instance.close()

    def input_username_handler(self):
        username = self.input_username.get()
        if len(username) > 9:
           self.error_display_or_destroy(message='your username must\n not exceed 9 characters !')
        elif not self.client_instance.connection():
            self.error_display_or_destroy(message='Connection failed')
        else:
            self.client_instance.username = username

        if self.client_instance.is_connected:
            self.error_display_or_destroy(destroy=True)

    def error_display_or_destroy(self, message='', destroy=False):
        if destroy:
            self.window.destroy()
        else:
            self.label_error['text'] = message

    def widget_for_username(self):
        welcome_label = Label(self.window, text='Welcome to Hajdaini chat :)', font='Arial 14 bold', bg=Gui.BG_COLOR, fg='#F71735')
        username_button = Button(self.window, font="Arial 12 bold", text="Apply", width="11", height=3,
                                  bd=0, bg="#F71735", fg='RosyBrown2', activebackground="#a51327",
                                  activeforeground='RosyBrown2', command=self.input_username_handler)
        self.label_error = Label(self.window, text='', font='Arial 14 bold', bg=Gui.BG_COLOR, fg='#FF6958')
        label_username = Label(self.window, text='Choose a username (9 characters max) ', font='Arial 12', bg=Gui.BG_COLOR, fg='white')
        self.input_username = Entry(self.window, font='Arial 12 bold', width=14, fg='#007EA7', border=2, justify='center')

        welcome_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        username_button.place(relx=0.5, rely=0.45, anchor=CENTER)
        label_username.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.input_username.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.label_error.place(relx=0.5, rely=0.6, anchor=CENTER)


if __name__ == '__main__':
    print("Please run client.py")
