{
    'name': "Kitabxana İdarəetmə Sistemi",
    'version': '18.0.1.0.0',
    'summary': "Odoo 18 üçün sadə kitabxana idarəetmə modulu.",
    'author': "Aim",  
    'website': "https://github.com/7aim",
    'category': 'Services/Library',
    'license': 'LGPL-3',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/assign_category_wizard_views.xml',
        'views/library_book_views.xml',
        'views/library_author_views.xml',
        'views/library_book_category_views.xml',
    ],

    'application': True,
    'installable': True,
}