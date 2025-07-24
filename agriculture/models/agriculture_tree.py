from odoo import models, fields, api

# Ağac
class AgricultureTree(models.Model):
    _name = 'agriculture.tree'
    _description = 'Təsərrüfat Ağacı'

    name = fields.Char(string="Ağac Kodu", required=True, copy=False, readonly=True, default=lambda self: 'Yeni')
    row_id = fields.Many2one('agriculture.row', string="Aid Olduğu Cərgə", required=True, ondelete='cascade')
    plot_id = fields.Many2one('agriculture.plot', string="Aid Olduğu Sahə", related='row_id.plot_id', store=True, readonly=True)
    
    plant_date = fields.Date(string="Əkilmə Tarixi")
    variety = fields.Char(string="Növü (Məs: Qızıləhmədi)")
    state = fields.Selection([
        ('young', 'Cavan'),
        ('productive', 'Məhsuldar'),
        ('sick', 'Xəstə'),
        ('removed', 'Çıxarılıb')
    ], string="Vəziyyəti", default='young')

    # Ağac nömrəsi
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Yeni') == 'Yeni':
                vals['name'] = self.env['ir.sequence'].next_by_code('agriculture.tree') or 'Yeni'
        return super().create(vals_list)