{
    'name': "Müştəri Dəstək Sistemi",
    'version': '1.0.0',
    'summary': "Müştəri müraciətlərini və ticketlərini idarə etmək üçün sistem.",
    'author': " Aim ",
    'website': "https://github.com/7aim",
    'category': 'Services/Helpdesk',
    'license': 'LGPL-3',

    'depends': ['base', 'mail', 'website'], 

    'data': [
        'security/ir.model.access.csv',
        'data/support_ticket_data.xml',
        'views/support_ticket_views.xml',
        'views/support_ticket_templates.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}