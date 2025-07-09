# -*- coding: utf-8 -*-
from odoo import models, fields, api

class QzModel(models.Model):
    _name = 'qz.model'
    _description = 'QZ Printer Test Model'

    name = fields.Char(string='Name', required=True, default="Test Product")
    total = fields.Float(string='Total', default=15.75)

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