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
    ],
    'assets': {
        'web.assets_backend': [
            'qebz_printer/static/src/js/qz_form_widget.js',
            'qebz_printer/static/src/xml/qz_form_widget_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
}