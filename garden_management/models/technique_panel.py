from odoo import models, fields, api

class TechniquePanel(models.Model):
    _name = 'technique.panel'
    _description = 'Texnika Paneli'
    _rec_name = 'name'

    name = fields.Char(string='Başlıq', required=True)
    car_no = fields.Char(string='Maşın Nömrəsi', required=True)

    type_of_equipment = fields.Selection(
        selection='_get_equipment_types',
        string='Texnika Növü'
    )
    type_of_brand = fields.Selection(
        selection='_get_brand_types',
        string='Marka'
    )
    type_of_fuel = fields.Selection([
        ('diesel', 'Dizel'), 
        ('petrol', 'Benzin'),
        ('electric', 'Elektrik'),
        ('hybrid', 'Hibrid')
    ], string='Yanacaq Növü')
    type_of_work = fields.Selection(
        selection='_get_work_types',
        string='İş Növü'
    )
    
    car_year = fields.Selection([
        ('2025', '2025'),('2024', '2024'),('2023', '2023'),('2022', '2022'),
        ('2021', '2021'),('2020', '2020'),('2019', '2019'),('2018', '2018'),
        ('2017', '2017'),('2016', '2016'),('2015', '2015'),('2014', '2014'),
        ('2013', '2013'),('2012', '2012'),('2011', '2011'),('2010', '2010')
    ], string='Araba İli')

    @api.model
    def _get_equipment_types(self):
        return self.env['soraqca.panel'].get_selection_items('texnika_novleri')
    
    @api.model
    def _get_brand_types(self):
        return self.env['soraqca.panel'].get_selection_items('marka')
    
    @api.model
    def _get_work_types(self):
        return self.env['soraqca.panel'].get_selection_items('is_novleri')