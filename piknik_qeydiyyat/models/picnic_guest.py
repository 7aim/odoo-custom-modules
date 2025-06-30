# -*- coding: utf-8 -*-

from odoo import models, fields

class PicnicGuest(models.Model):
    _name = 'picnic.guest'
    _description = 'Piknik Qonağı'
    _order = 'id'

    name = fields.Char(string="Qonağın Adı", required=True)
    entry_id = fields.Many2one('picnic.entry', string='Giriş Qeydi', ondelete='cascade', required=True)