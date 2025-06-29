# -*- coding: utf-8 -*-

from odoo import models, fields

class PicnicZone(models.Model):
    _name = 'picnic.zone'
    _description = 'Piknik Zonası'
    _order = 'name' # Zonaları adlarına görə sıralayacaq

    name = fields.Char(string="Zonanın Adı", required=True)
    
    # Eyni adda ikinci zona yaratmağın qarşısını almaq üçün
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Bu adda zona artıq mövcuddur!')
    ]