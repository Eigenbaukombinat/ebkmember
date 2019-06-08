from email.message import EmailMessage
from mailconfig import SERVER, PORT, USER, PW, FROM, TO, URL, CC
import calendar
import datetime
import smtplib
import sqlite3
import sys
import transaction

def db(func):
    def func_wrapper(*args, **kw):
        db = sqlite3.connect('db.sqlite3')
        db.row_factory = sqlite3.Row
        c = db.cursor()
        res = func(c, *args, **kw)
        db.commit()
        db.close()
        return res
    return func_wrapper


@db
def get_new_registrations(c):
    c.execute("SELECT * FROM registration_member where status='exported'");
    return c.fetchall()


@db
def change_status_to_mailsent(c, reg_id):
    c.execute("UPDATE registration_member SET status='mail_sent' where id=(?)", (reg_id,))


new_regs = get_new_registrations()
if not new_regs:
    sys.exit(0)



def send_mail(reg):
    with open('mailtemplate.in', 'r') as templatefile:
        template = templatefile.readlines()
    msg = EmailMessage()
    msg.set_content(''.join(template[1:]).format(**reg))

    msg['Subject'] = template[0].strip()
    msg['From'] = FROM
    msg['To'] = reg['email']
    msg['CC'] = TO 

    s = smtplib.SMTP(SERVER, PORT)
    if (USER and PW):
        s.login(USER, PW)
    s.send_message(msg)
    s.quit()


for reg in new_regs:
    send_mail(reg)
    change_status_to_mailsent(reg['id'])

