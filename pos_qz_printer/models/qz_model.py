from odoo import models, fields, api

class QzModel(models.Model):
    _name = 'qz.model'
    _description = 'QZ Printer Test Model'

    # Basliq ve qiymet
    name = fields.Char(string='Name', required=True, default="Test Product")
    total = fields.Float(string='Total', default=15.75)

    # "Print Receipt" butonu
    def action_print_receipt(self):
        """QZ Tray ilə çap etmə funksiyası"""
        return {
            'type': 'ir.actions.client',
            'tag': 'print_qz_receipt',
            'params': {
                'name': self.name,
                'total': self.total,
            }
        }