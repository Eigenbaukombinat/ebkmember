import sqlite3
import smtplib
from email.message import EmailMessage
import sys
from mailconfig import SERVER, PORT, USER, PW, FROM, TO, URL, CC
from mailer import send_mail

def db(func):
    def func_wrapper(*args, **kw):
        db = sqlite3.connect('db.sqlite3')
        c = db.cursor()
        res = func(c, *args, **kw)
        db.commit()
        db.close()
        return res
    return func_wrapper


@db
def get_new_registrations(c):
    c.execute("SELECT * FROM registration_member where status='pending'");
    return c.fetchall()

new_regs = get_new_registrations()
if not new_regs:
    sys.exit(0)

msg = EmailMessage()
msg.set_content("""Es gibt {} neue Mitgliedsanträge.

@Kassenwarte: Bitte verifizieren!

{}

Anträge mit dem Status "pending" anklicken, Daten prüfen, das "Entrydate" (=Eintrittsdatum -> "heute" falls es keinen besonderen Grund gibt) setzen und den Status auf "approved" setzen. Danach im collmex gucken ob das Mitglied dort richtig ankommt. Falls nicht, nilo nerven.
""".format(len(new_regs), URL))

msg['Subject'] = 'Neue Online-Mitgliedsanträge'
msg['From'] = FROM
msg['To'] = TO
if CC:
    msg['CC'] = CC
send_mail(msg)
