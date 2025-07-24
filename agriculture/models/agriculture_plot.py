from odoo import models, fields, api

# Sahə
class AgriculturePlot(models.Model):
    _name = 'agriculture.plot'
    _description = 'Təsərrüfat Sahəsi'

    name = fields.Char(string="Sahənin Adı", required=True)
    area = fields.Float(string="Sahə (hektar)")
    location = fields.Char(string="Yerləşdiyi Ünvan")
    
    row_ids = fields.One2many('agriculture.row', 'plot_id', string="Cərgələr")
    row_count = fields.Integer(string="Cərgə Sayı", compute='_compute_row_count')
    tree_count = fields.Integer(string="Ümumi Ağac Sayı", compute='_compute_tree_count')

    @api.depends('row_ids')
    def _compute_row_count(self):
        for plot in self:
            plot.row_count = len(plot.row_ids)

    @api.depends('row_ids.tree_count')
    def _compute_tree_count(self):
        for plot in self:
            plot.tree_count = sum(row.tree_count for row in plot.row_ids)