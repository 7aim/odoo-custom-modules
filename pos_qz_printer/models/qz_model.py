from odoo import models, fields, api

class QZPrintTest(models.Model):
    _name = 'qz.print.test'
    _description = 'QZ Yazıcı Testi'

    name = fields.Char(string="Ad")
    total = fields.Float(string="Tutar")

    def action_print_receipt(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'print_qz_receipt',
            'params': {
                'name': self.name,
                'total': self.total,
            }
        }
