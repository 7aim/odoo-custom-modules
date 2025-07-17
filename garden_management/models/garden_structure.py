from odoo import models, fields

class GardenArea(models.Model):
    _name = 'garden.area'
    _description = 'Sahə' # Bu ən üst səviyyədir, ona görə başqa modelə bağlanmır

    name = fields.Char(string='Sahənin Adı', required=True)

class GardenTerritory(models.Model):
    _name = 'garden.territory'
    _description = 'Ərazi'

    name = fields.Char(string='Ərazinin Adı', required=True)

    area_id = fields.Many2one(
        comodel_name='garden.area',
        string='Sahə',
        ondelete='set null' # Əgər sahə silinərsə, bu sahə boş qalacaq
        #ondelete='cascade' # Əgər sahə silinərsə, bu ərazi də silinəcək
        #ondelete='restrict' # Əgər sahə silinərsə, bu ərazi silinə bilməz
    )

class GardenRegion(models.Model):
    _name = 'garden.region'
    _description = 'Bölgə'

    name = fields.Char(string='Bölgənin Adı', required=True)

    territory_id = fields.Many2one(
        comodel_name='garden.territory',
        string='Ərazi',
        ondelete='set null'
    )

    area_id = fields.Many2one(
        'garden.area', 
        string='Sahə', 
        related='territory_id.area_id', 
        store=True)
    
class GardenSubRegion(models.Model):
    _name = 'garden.subregion'
    _description = 'Kiçik Bölgə'

    name = fields.Char(string='Kiçik Bölgənin Adı', required=True)

    region_id = fields.Many2one(
        comodel_name='garden.region',
        string='Bölgə',
        ondelete='set null'
    )

    territory_id = fields.Many2one(
        'garden.territory', 
        string='Ərazi',
        related='region_id.territory_id',
        store=True)
        
    area_id = fields.Many2one(
        'garden.area',
        string='Sahə',
        related='region_id.area_id',
        store=True)