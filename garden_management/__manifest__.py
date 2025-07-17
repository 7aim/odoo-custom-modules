{
    'name': "Bağçılıq İdarəetməsi", 

    'summary': """
        Bağçılıq və kənd təsərrüfatı fəaliyyətlərinin idarə olunması üçün modul.
    """,

    'author': "Aim",
    'website': "https://github.com/7aim/garden_management",

    'category': 'Operations/Agriculture',
    'version': '18.0.1.0.0',

    'depends': ['base', 'mail', 'hr'],

    'data': [
        'security/ir.model.access.csv',
        
        'views/paneller/garden_structure_views.xml',
        'views/paneller/suvarma_panel_views.xml', 

        'views/diger_paneller/garden_problem_panel.xml',
        'views/diger_paneller/technique_panel_views.xml',
        'views/diger_paneller/soraqca_panel_views.xml', 
        'views/diger_paneller/fruits_panel_views.xml', 
        'views/diger_paneller/gubre_panel_views.xml',  
    ],

    'application': True, 
    'installable': True,
}