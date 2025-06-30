{
    'name': 'XPrinter POS Integration',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Adds XPrinter support to POS via a direct printing service',
    'description': """X-Printer ESC/POS desteği""",
    'author': 'Sahib Akbar',
    'depends': ['point_of_sale', 'direct_print_interface'], # direct_print_interface'i ekleyin
    'assets': {
        'point_of_sale.assets': [
            'xprinter_module/static/src/js/xprinter.js',
        ],
    },
    'installable': True,
    'application': True, # Bunu False yapın
}