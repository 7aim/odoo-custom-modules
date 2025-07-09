# pos_qz_printer/__manifest__.py

{
    'name': 'POS QZ Printer',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Integrate QZ Tray printer with Odoo POS',
    'author': 'Sizin Adınız',
    'depends': ['web', 'point_of_sale'],
    'data': [
        # 'security/ir.model.access.csv', # Ehtiyac varsa, bu sətri aktiv saxlayın
        'security/ir.model.access.csv',
        'views/qz_model_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_qz_printer/static/src/js/qz_printer.js',
        ],
        'web.assets_qweb': [
            'pos_qz_printer/static/src/xml/qz_printer_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
}