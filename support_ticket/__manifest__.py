{
    'name': "Müştəri Dəstək Sistemi",
    'version': '1.0.0',
    'summary': "Müştəri müraciətlərini və ticketlərini idarə etmək üçün sistem.",
    'author': " Aim ",
    'website': "https://github.com/7aim",
    'category': 'Services/Helpdesk',
    'license': 'LGPL-3',

    # Modulun işləməsi üçün tələb olunan digər modullar
    'depends': ['base', 'mail'],  # 'website'-i çıxarın əgər lazım deyilsə

    # Modul yüklənəndə Odoo tərəfindən oxunacaq faylların siyahısı
    'data': [
        'security/ir.model.access.csv',
        'views/support_ticket_views.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,  # Əlavə edin
}