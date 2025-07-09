{
    'name': 'Custom QZ Printer',
    'summary': 'QZ Tray ile özel yazdırma işlemi',
    'version': '1.0',
    'author': 'Sen',
    'depends': ['base', 'web'],
    'data': [
        'views/qz_model_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_qz_printer/static/src/js/qz_printer.js',
        ],
    },
    'installable': True,
    'application': True,
}
