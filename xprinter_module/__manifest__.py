{
    'name': 'XPrinter Integration',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'XPrinter üçün POS çap modulu',
    'description': """X-Printer ESC/POS dəstəyi""",
    'author': 'Sahib Akbar',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale.assets': [
            'xprinter_module/static/src/js/xprinter.js',
        ],
    },
    'installable': True,
    'application': True,
}
