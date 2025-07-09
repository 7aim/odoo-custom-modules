# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QzModel(models.Model):
    _name = 'qz.model'
    _description = 'QZ Printer Test Model'

    name = fields.Char(string='Name', required=True, default="Test Product")
    total = fields.Float(string='Total', default=15.75)

    def action_print_receipt(self):
        """
        This method prepares the data and returns a client action
        to trigger the QZ Tray printing.
        """
        self.ensure_one()

        # JavaScript-ə göndəriləcək parametrlər
        params = {
            'name': self.name,
            'total': self.total,
        }

        return {
            'type': 'ir.actions.client',
            'tag': 'print_qz_receipt', # Bu ad JS faylındakı ad ilə eyni olmalıdır
            'params': params,
        }