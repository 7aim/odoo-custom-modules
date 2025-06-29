# -*- coding: utf-8 -*-
{
    'name': "Piknikə Giriş Modulu",
    'summary': """
        Piknik ərazisinə daxil olan şəxslərin və maşınların qeydiyyatı.
    """,
    'description': """
        Bu modul piknik sahəsinə girişləri qeydə almaq üçün istifadə olunur.
        Funksionallıq: Maşın nömrəsi, Adam sayı, Adlar, Giriş-çıxış vaxtı, Zona, Ödəniş, Qəbul edən şəxs.
    """,
    'author': "Sizin Adınız",
    'website': "https://www.sizin-websaytiniz.com",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/picnic_entry_views.xml',
        'views/picnic_zone_views.xml', 
        'views/accepting_person_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}