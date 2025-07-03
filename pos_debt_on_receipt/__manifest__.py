# -*- coding: utf-8 -*-
{
    'name': 'POS - Köhnə Borcun Çekdə Göstərilməsi',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Müştərinin ümumi borcunu Point of Sale çekində göstərir.',
    'description': """
        Bu modul Odoo 18 Point of Sale üçün hazırlanmışdır.
        Funksionallığı:
        - POS-da müştəri seçildikdə onun mühasibatlıqdakı ümumi borcunu hesablayır.
        - Bu borcu ödənişdən sonra çap olunan çekdə "Köhnə Borc" başlığı ilə göstərir.
    """,
    'author': 'Sizin Adınız və ya Şirkətinizin Adı',
    'website': 'https://sizin-vebsaytiniz.com',
    'depends': [
        'point_of_sale',
        'account'  # Borcu hesablamaq üçün 'account' modulundan asılıyıq
    ],
    'data': [
        # Bu hissəyə XML faylını sonra əlavə edəcəyik
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_debt_on_receipt/static/src/pos_receipt.js',
            'pos_debt_on_receipt/static/src/pos_receipt.xml',
        ],
    },
    
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}