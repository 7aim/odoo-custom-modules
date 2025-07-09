{
    'name': "Xərc İdarəetmə Sistemi",
    'version': '18.0.1.0.0',
    'summary': "İşçilərin xərclərini idarə etmək və mühasibatlığa inteqrasiya etmək üçün modul.",
    'author': "Aim",
    'website': "https://github.com/7aim", 
    'category': 'Human Resources/Expenses',
    'license': 'LGPL-3',

    'depends': ['base', 'mail', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/expense_report_views.xml',
    ],

    'application': True,
    'installable': True,
}