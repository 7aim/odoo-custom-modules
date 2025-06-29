# -*- coding: utf-8 -*-

from odoo import models, fields

class AcceptingPerson(models.Model):
    _name = 'accepting.person'
    _description = 'Qebul eden şexs'
    _order = 'name' 

    name = fields.Char(string="Qebul eden şexsin adı", required=True)
    
    # Eyni adda ikinci sexsi yaratmağın qarşısını almaq üçün
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Bu adda şexs artıq mövcuddur!')
    ]