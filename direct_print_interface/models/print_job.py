# -*- coding: utf-8 -*-
from odoo import models, fields

class PrintJob(models.Model):
    _name = 'direct.print.job'
    _description = 'Direct Print Job Queue'

    data_to_print = fields.Text("Data to Print", required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('printed', 'Printed'),
        ('failed', 'Failed'),
    ], string="Status", default='pending', required=True)
    printer_name = fields.Char("Printer Name", help="The name of the target local printer.", default="Xprinter XP-Q80C")