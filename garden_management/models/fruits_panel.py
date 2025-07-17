# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FruitsPanel(models.Model):
    _name = 'fruits.panel'
    _description = 'Meyvə Paneli'
    _rec_name = 'name'

    name = fields.Char(string='Meyvenin adı', required=True)

    active = fields.Boolean(string='Aktiv', default=True)