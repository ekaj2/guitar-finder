import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path
from getpass import getpass


class Emailer:
    """Complete class for sending an email with HTML and plain text to a list of subscribers.

    Methods:
        __init__: Initializes self.msg, self.recipients, then sends the email.
        load_text: Attaches the text part of the email after reading from a specified file.
        load_html: Attaches the HTML part of the email after reading from a specified file.
        login_to_server: Attempts to login to the SMTP server with email and password.
        send: Sends the email to the recipients in the subscription list.
    """

    def __init__(self, text, html, newsletter=None):
        """Initializes self.msg, self.recipients, then starts the interaction with self.start()."""

        self.msg = MIMEMultipart('alternative')
        self.newsletter = newsletter
        self.text = text
        self.html = html

        self.msg['From'], self.msg['To'], self.pw = self.get_info()
        self.msg['Subject'] = "Guitar Search"

        self.load_text()
        self.load_html()

        # login and send the email
        self.send()

    def load_text(self):
        """Attaches the text part of the email after reading from a specified file."""
        if self.newsletter:
            with open(self.newsletter + ".txt", 'r') as t:
                self.setup_text(t.read())
        else:
            self.setup_text(self.text)

    def setup_text(self, text):
        part1 = MIMEText(text, 'plain')
        self.msg.attach(part1)

    def load_html(self):
        """Attaches the HTML part of the email after reading from a specified file."""
        if self.newsletter:
            with open(self.newsletter + ".html", 'r') as h:
                self.setup_html(h.read())
        else:
            self.setup_html(self.html)

    def setup_html(self, html):
        part2 = MIMEText(html, 'html')
        self.msg.attach(part2)

    def login_to_server(self, server):
        try:
            server.login(self.msg['From'], self.pw)
        except smtplib.SMTPAuthenticationError:
            print("Invalid password!")
            exit()

    def send(self):
        # Send the message via local SMTP server.
        with smtplib.SMTP('smtp.ipage.com') as server:
            self.login_to_server(server)
            server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            server.quit()

    def get_info(self):
        # we need to provide all three of these
        msg_from = None
        msg_to = None
        msg_pw = None

        if not os.path.isfile("info.txt"):
            # prompt user for info
            msg_from = input("From: ")
            msg_to = input("To: ")
            print("This password is not protected...enter at your own risk!")
            msg_pw = getpass("From password: ")  # this is not protected...use a dummy email account

            # write info to file
            with open("info.txt", 'w') as f:
                print("msg_from:{f}\nmsg_to:{t}\nmsg_pw:{p}".format(f=msg_from, t=msg_to, p=msg_pw), file=f)

        # get data from file
        with open("info.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("msg_from:"):
                    msg_from = line[line.find("msg_from"):]
                elif line.startswith("msg_to:"):
                    msg_from = line[line.find("msg_to"):]
                elif line.startswith("msg_pw:"):
                    msg_from = line[line.find("msg_pw"):]

        # ensure we have the data
        if any((msg_from, msg_pw, msg_to)) is None:
            print("INVALID FILE!!!")
        return msg_from, msg_to, msg_pw


def main():
    Emailer("This is a test", "This is a test")


if __name__ == '__main__':
    main()
