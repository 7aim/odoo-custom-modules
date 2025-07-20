from odoo import models, fields, api

class SoraqcaPanel(models.Model):
    _name = 'soraqca.panel'
    _description = 'Soraqça Paneli'
    _rec_name = 'name'

    name = fields.Char(string='Ad', required=True)
    panel_type = fields.Selection([
        ('is_novleri', 'İş Növləri'),
        ('texnika_novleri', 'Texnika Növləri'),
        ('marka', 'Marka'),
        ('problem_novleri', 'Problem Növləri'),
    ], string='Panel Tipi', required=True)
    
    active = fields.Boolean(string='Aktiv', default=True)
    
    @api.model
    def get_selection_items(self, panel_type):
        """Müəyyən panel tipi üçün selection items qaytarır"""
        items = self.search([('panel_type', '=', panel_type), ('active', '=', True)])
        return [(item.name.lower().replace(' ', '_'), item.name) for item in items]