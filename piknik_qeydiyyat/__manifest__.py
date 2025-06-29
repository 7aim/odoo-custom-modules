# -*- coding: utf-8 -*-
{
    'name': "Piknikə Giriş Modulu",
    'summary': "Piknik ərazisinə daxil olan şəxslərin və maşınların qeydiyyatı.",
    'author': "Asim",
    'website': "https://github.com/7aim/odoo-custom-modules/tree/main/piknik_qeydiyyat",
    'category': 'Uncategorized',
    'version': '1.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml', 
        'report/picnic_reports.xml',
        'report/picnic_report_templates.xml',
        'views/picnic_entry_views.xml',
        'views/picnic_zone_views.xml',
        'views/accepting_person_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}