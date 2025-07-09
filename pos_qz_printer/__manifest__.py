{
    'name': 'POS QZ Printer',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Integrate QZ Tray printer with Odoo POS',
    'author': 'Aim',
    'depends': ['web', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/qz_model_views.xml',
        'views/print_job_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_qz_printer/static/src/js/qz_printer.js',
            'pos_qz_printer/static/src/xml/qz_printer_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
}