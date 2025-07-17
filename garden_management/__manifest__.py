{
    'name': "Bağçılıq İdarəetməsi", 

    'summary': """
        Bağçılıq və kənd təsərrüfatı fəaliyyətlərinin idarə olunması üçün modul.
    """,

    'author': "Aim",
    'website': "https://www.github.com/7aim/garden_management",

    'category': 'Operations/Agriculture',
    'version': '18.0.1.0.0',

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/garden_structure_views.xml',
        'views/garden_problem_panel.xml',
        'views/technique_panel_views.xml',
        'views/soraqca_panel_views.xml', 
        'views/fruits_panel_views.xml', 
    ],

    'application': True, 
    'installable': True,
}