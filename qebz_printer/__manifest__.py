{
    'name': 'Qebz Printer',
    'version': '1.0',
    'category': '',
    'summary': 'Integrate QZ Tray printer with Odoo POS',
    'author': 'Aim',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/qz_model_views.xml',
        'views/qz_receipt_templates.xml',

    ],
    'assets': {
        'point_of_sale.assets': [ 
            'pos_qz_printer/static/src/js/qz-tray.js', # QZ kitabxanası
            'pos_qz_printer/static/src/js/pos_integration.js',
    ],

    },
    'installable': True,
    'application': True,
}