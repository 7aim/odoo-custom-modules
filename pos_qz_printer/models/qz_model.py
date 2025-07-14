from odoo import models, fields, api

class QzModel(models.Model):
    _name = 'qz.model'
    _description = 'QZ Printer Test Model'

    name = fields.Char(string='Name', required=True, default="Test Product")
    total = fields.Float(string='Total', default=15.75)