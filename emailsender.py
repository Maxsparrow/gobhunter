import smtplib
from email.mime.text import MIMEText
from connections import email_user, email_pass


def send_email(from_addr, to_addrs, subject, message_body, username, password):
    msg = MIMEText(message_body, 'html')
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Subject'] = subject
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()


if __name__ == '__main__':
    message_body = "I'm a robot lol<br><br><strong>Testing bold</strong>"
    send_email(email_user + '@gmail.com', ['maxsparrow@gmail.com'], "I can send email from my program!",
               message_body, email_user, email_pass)


