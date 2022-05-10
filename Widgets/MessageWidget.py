from tkinter import Label, Text, INSERT, WORD
from Widgets.BaseWidget import BaseWidget
import imaplib
import email
from email.header import decode_header


class MessageWidget(BaseWidget):
    app_pass_path = "config/MessageWidget/AppPassword.txt"

    def get_app_pass(self):
        with open(self.app_pass_path, "r") as f:
            return f.read()

    def __init__(self, parent, subwidgets=[], constraints=[], props={}):
        BaseWidget.__init__(self, parent, subwidgets, constraints, props)
        self.config(bg=self.get_bg())
        self.msg_text = Text(self, bg=self.get_bg())
        self.username = "jasmynsmirror@gmail.com"
        self.password = self.get_app_pass()
        self.message_dimensions = (self.width, self.height)
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        self.imap.login(self.username, self.password)
        self.msg = ""
        self.sender = ""
        self.last_msg = ""
        self.update_values()

    def login(self):
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        self.imap.login(self.username, self.password)

    def place(self, *args, **kargs):
        self.update_dimensions()
        BaseWidget.place(self, *args, **kargs)
        self.draw_message()

    def draw_message(self):
        message = f"{self.msg} ({self.sender})\n\n"
        if message != self.last_msg:
            # self.msg_text.config(text=message)
            self.msg_text.config(fg=self.get_fg())
            # set font
            self.msg_text.config(font=self.get_font("huge"), wrap=WORD)
            self.msg_text.config(highlightthickness=0, bd=0, )
            self.msg_text.insert("1.0", message)
            self.msg_text.pack()
            self.last_msg = message

    def update_dimensions(self):
        self.message_dimensions = (self.width, self.height)

    def update_values(self):
        status, messages = self.imap.select("INBOX")
        # number of top emails to fetch
        N = 1
        # total number of emails
        messages = int(messages[0])
        for i in range(messages, messages-N, -1):
        # fetch the email message by ID
            
            res, msg = self.imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    print("Subject:", subject)
                    print("From:", From)
                    self.msg = subject
                    self.sender = From
                        