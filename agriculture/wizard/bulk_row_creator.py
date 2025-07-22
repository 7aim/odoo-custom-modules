# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BulkRowCreator(models.TransientModel):
    _name = 'agriculture.bulk.row.creator'
    _description = 'Toplu Cərgə Yaradıcısı'

    plot_id = fields.Many2one('agriculture.plot', string="Sahə", required=True)
    row_count = fields.Integer(string="Cərgə Sayı", required=True, default=10)
    trees_per_row = fields.Integer(string="Hər Cərgədə Ağac Sayı", required=True, default=20)
    
    # Cərgə adlandırma
    row_prefix = fields.Char(string="Cərgə Prefiksi", help="Məs: 'A' -> A1, A2, A3...")
    use_plot_code = fields.Boolean(string="Sahə Kodunu İstifadə Et", default=True)
    
    # Ağac məlumatları
    tree_variety = fields.Char(string="Ağac Növü", default="Qızıləhmədi")
    plant_date = fields.Date(string="Əkilmə Tarixi", default=fields.Date.context_today)

    @api.onchange('plot_id')
    def _onchange_plot_id(self):
        if self.plot_id:
            # Sahə adından ilk hərfi götür
            if self.plot_id.name:
                self.row_prefix = self.plot_id.name[0].upper()

    def action_create_rows(self):
        """Toplu cərgə və ağac yaradır"""
        created_rows = []
        
        for i in range(1, self.row_count + 1):
            # Cərgə adı yarad
            if self.use_plot_code and self.row_prefix:
                row_name = f"{self.row_prefix}{i}"
            else:
                row_name = f"Cərgə {i}"
            
            # Cərgə yarat
            row = self.env['agriculture.row'].create({
                'name': row_name,
                'plot_id': self.plot_id.id,
            })
            created_rows.append(row)
            
            # Həmin cərgə üçün ağaclar yarat
            trees_to_create = []
            for j in range(1, self.trees_per_row + 1):
                trees_to_create.append({
                    'row_id': row.id,
                    'variety': self.tree_variety,
                    'plant_date': self.plant_date,
                    'state': 'young',
                })
            
            # Toplu ağac yaratma
            if trees_to_create:
                self.env['agriculture.tree'].create(trees_to_create)
        
        # Nəticə göstər
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Uğur!',
                'message': f'{len(created_rows)} cərgə və {len(created_rows) * self.trees_per_row} ağac yaradıldı.',
                'type': 'success',
            }
        }

    def action_preview(self):
        """Yaradılacaq cərgələrin preview-nu göstər"""
        preview_list = []
        
        for i in range(1, min(self.row_count + 1, 6)):  # İlk 5-ni göstər
            if self.use_plot_code and self.row_prefix:
                row_name = f"{self.row_prefix}{i}"
            else:
                row_name = f"Cərgə {i}"
            preview_list.append(row_name)
        
        if self.row_count > 5:
            preview_list.append("...")
        
        preview_text = ", ".join(preview_list)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Preview',
                'message': f'Yaradılacaq cərgələr: {preview_text}\\nHər cərgədə {self.trees_per_row} ağac olacaq.',
                'type': 'info',
            }
        }
