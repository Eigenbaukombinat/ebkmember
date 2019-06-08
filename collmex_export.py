import datetime
import sys
import calendar
from gocept.collmex.collmex import Collmex
from gocept.collmex.model import Member, MemberProduct
import sqlite3
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
    c.execute("SELECT * FROM registration_member where status='approved'");
    return c.fetchall()


@db
def change_status_to_exported(c, reg_id):
    c.execute("UPDATE registration_member SET status='exported' where id=(?)", (reg_id,))


new_regs = get_new_registrations()
if not new_regs:
    sys.exit(0)

api = Collmex()

mapping = [
    ('name','Vorname'),
    ('surname','Name'),
    ('postcode','PLZ'),
    ('location','Ort'),
    ('country','Land'),
    ('email','E-Mail'),
    ('phonenumber','Telefon'),
    ('birthdate','Geburtsdatum'),
    ('entrydate','Eintrittsdatum'),
    ('iban','Iban'),
]


#('fee',''),
#('memberstatus',''),

status_mapping = {
        'member': (1, 24),
        'sustaining_member':  (3, 18),
        'junior_member':  (4, 8)
        }


for reg in new_regs:
    #find next free mitgliedsnummer
    mems = api.get_members(include_inactive=True)
    custs = api.get_customers()
    custids = [int(cust['Kundennummer']) for cust in custs]
    memids = [int(mem['Mitgliedsnummer']) for mem in mems]
    new_memid = str(max(memids + custids) + 1)
    member = Member()
    member['Mitgliedsnummer'] = new_memid
    for regf, cmf in mapping:
        member[cmf] = reg[regf]
    member['Straße'] = '{} {}'.format(reg['street'], reg['streetnumber'])
    api.create(member)
    transaction.commit()
    entry_dt = datetime.date(*[int(t) for t in reg['entrydate'].split('-')])
    valid_from = reg['entrydate']
    pos = 1
    if entry_dt.day != 1:
        #anteiligen beitrag anlegen
        days = calendar.monthrange(entry_dt.year, entry_dt.month)[1]
        factor = entry_dt.day / float(days)
        beitrag = MemberProduct()
        beitrag['Mitglieds-Nr'] = new_memid
        beitrag['Pos'] = 1
        pos = 2
        beitrag['Firma'] = 1
        beitrag['Gültig von'] = reg['entrydate']
        #beitrag['Gültig bis'] = (datetime.date(entry_dt.year, entry_dt.month, days) + datetime.timedelta(days=1)).isoformat()
        beitrag['Gültig bis'] = datetime.date(entry_dt.year, entry_dt.month, days).isoformat()
        beitrag['Intervall'] = 3 #monat 
        beitrag['Nächste Rechnung'] = reg['entrydate']
        prodid, defaultfee = status_mapping[reg['memberstatus']]
        beitrag['Produkt Nr'] = prodid
        beitrag['Individueller Preis'] = str(reg['fee'] - (reg['fee'] * factor)).replace('.',',')
        api.create(beitrag)
        valid_from = (datetime.date(entry_dt.year, entry_dt.month, days) + datetime.timedelta(days=1)).isoformat()
    #    next_invoice = datetime.date(entry_dt.year, entry_dt.month, days).isoformat() 
    #else:
    #    next_invoice = (entry_dt - datetime.timedelta(days=1)).isoformat()
    beitrag2 = MemberProduct()
    beitrag2['Mitglieds-Nr'] = new_memid
    beitrag2['Firma'] = 1
    beitrag2['Pos'] = pos 
    beitrag2['Gültig von'] = valid_from
    beitrag2['Gültig bis'] = '31.12.9999'
    beitrag2['Intervall'] = 3 #monat 
    beitrag2['Nächste Rechnung'] = valid_from 
    prodid, defaultfee = status_mapping[reg['memberstatus']]
    beitrag2['Produkt Nr'] = prodid
    if int(reg['fee']) != defaultfee:
        beitrag2['Individueller Preis'] = str(reg['fee']).replace('.',',')
    api.create(beitrag2)
    change_status_to_exported(reg['id'])
    transaction.commit()
