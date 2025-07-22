# -*- coding: utf-8 -*-
{
    'name': "Kənd Təsərrüfatı İdarəetməsi",
    'summary': """
        Sahələr, cərgələr, ağaclar və təsərrüfat əməliyyatlarının idarə edilməsi.
    """,
    'description': """
        Bu modul kənd təsərrüfatı fəaliyyətlərini izləmək üçün nəzərdə tutulub.
        - Sahələrin qeydiyyatı
        - Cərgələrin idarə edilməsi
        - Ağacların və onların vəziyyətinin izlənilməsi
    """,
    'author': "Sizin Adınız",
    'website': "https://www.sizinvebsayt.com",
    'category': 'Industries',
    'version': '18.0.1.0.6',
    'depends': ['base', 'stock', 'purchase'],  
    'data': [
        'security/ir.model.access.csv',
        'data/operation_types.xml',
        'views/agriculture_plot_views.xml',
        'views/agriculture_row_views.xml',
        'views/agriculture_tree_views.xml',
        'views/agriculture_operation_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True, 
    'license': 'LGPL-3',
}