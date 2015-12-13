import smtplib
from connections import email_user, email_pass


def send_email(from_addr, to_addrs, subject, message_body, username, password):
    message = "\r\n".join([
        "From: %s" % from_addr,
        "To: %s" % ", ".join(to_addrs),
        "Subject: %s" % subject,
        "",
        message_body
    ])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message)
    server.quit()


if __name__ == '__main__':
    message_body = "I'm a robot lol"
    send_email(email_user + '@gmail.com', ['maxsparrow@gmail.com'], "I can send email from my program!",
               message_body, email_user, email_pass)


