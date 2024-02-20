#coding:utf8
SEX = (
    ('male','Mann'),
    ('female', 'Frau'),
    ('other', 'other'),
    )

MEMBERSTATUS = (
    ('member','Mitglied'),
    ('sustaining_member', 'Fördermitglied'),
    ('junior_member', 'Juniormitglied'),
    )

STATUS = (
    ('pending','pending'),
    ('approved','approved'),
    ('rejected','rejected'),
    ('exported','exported'),
    ('mail_sent','mail_sent'),
    )

FEE = (
    (30, 'normal'),
    (23, 'reduced'),
    (5,'sustain_min'),
    (0, 'other'),
    (5, 'sustain_other'),
    (8, 'junior'),
    (8, 'junior_other'),
)
