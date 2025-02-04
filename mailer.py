from mailconfig import SERVER, PORT, USER, PW
import smtplib, ssl


def send_mail(msg):
    s = smtplib.SMTP(SERVER, PORT)
    if (USER and PW):
        s.login(USER, PW)
    s.send_message(msg)
    s.quit()

def send_mail(msg):
    context=ssl.create_default_context()

    with smtplib.SMTP(SERVER, port=PORT) as smtp:
        smtp.starttls(context=context)
        smtp.login(USER, PW)
        smtp.send_message(msg)
