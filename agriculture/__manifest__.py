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
    'version': '18.0.2.0.0',
    'depends': ['base', 'stock', 'purchase'],  
    'data': [
        'security/ir.model.access.csv',
        'data/operation_types.xml',
        'wizard/bulk_row_creator_views.xml',
        'views/agriculture_plot_views.xml',
        'views/agriculture_row_views.xml',
        'views/agriculture_tree_views.xml',
        'views/agriculture_operation_views.xml',
        'views/agriculture_worker_views.xml',
        'views/agriculture_worker_dashboard.xml',
        'views/agriculture_pivot_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True, 
    'license': 'LGPL-3',
}