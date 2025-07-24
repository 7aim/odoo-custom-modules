from odoo import models, fields, api

# Cərgə
class AgricultureRow(models.Model):
    _name = 'agriculture.row'
    _description = 'Sahədəki Cərgə'

    name = fields.Char(string="Cərgə Nömrəsi/Adı", required=True)
    plot_id = fields.Many2one('agriculture.plot', string="Aid Olduğu Sahə", required=True, ondelete='cascade')
    
    tree_ids = fields.One2many('agriculture.tree', 'row_id', string="Ağaclar")
    tree_count = fields.Integer(string="Ağac Sayı", compute='_compute_tree_count')

    @api.depends('tree_ids')
    def _compute_tree_count(self):
        for row in self:
            row.tree_count = len(row.tree_ids)