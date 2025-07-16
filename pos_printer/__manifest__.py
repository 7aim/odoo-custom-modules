{
    'name': 'Custom Printer Module',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Custom Printer API for any Odoo module',
    'author': 'Aim',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_printer_views.xml',
    ],
    'installable': True,
    'application': True,
}