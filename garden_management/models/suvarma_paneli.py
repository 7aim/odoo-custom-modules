from odoo import models, fields, api

class SaygacPanel(models.Model):
    _name = 'saygac.panel'
    _description = 'Sayğac Paneli'
    _rec_name = 'name'

    name = fields.Char(string='Sayğacın adı', required=True)
    description = fields.Text(string='Təsvir')


class KranPanel(models.Model):
    _name = 'kran.panel'
    _description = 'Kran Paneli'
    _rec_name = 'name'

    name = fields.Char(string='Kranın adı', required=True)

    saygac_id = fields.Many2one('saygac.panel', string='Sayğac', required=True)

    subregion_id = fields.Many2one('garden.subregion', string='Kiçik Bölgə')
    region_id = fields.Many2one('garden.region', string='Bölgə', related='subregion_id.region_id', store=True)
    territory_id = fields.Many2one('garden.territory', string='Ərazi', related='subregion_id.territory_id', store=True)
    area_id = fields.Many2one('garden.area', string='Sahə', related='subregion_id.area_id', store=True)
    rows = fields.Char(string='Cərgələr')

    manufacturer_id = fields.Many2one('hr.employee', string='Istehsalçı')

    create_date = fields.Date(string='Qurulma Tarixi', default=fields.Date.today)

class SuvarmaPanel(models.Model):
    _name = 'suvarma.panel'
    _description = 'Suvarma Paneli'
    _rec_name = 'name'

    name = fields.Char(string='Suvarmanın adı', required=True)
    description = fields.Text(string='Qeyd')

    kran_id = fields.Many2one('kran.panel', string='Kran', required=True)

    subregion_id = fields.Many2one('garden.subregion', string='Kiçik Bölgə', related='kran_id.subregion_id', store=True, readonly=True)
    region_id = fields.Many2one('garden.region', string='Bölgə', related='kran_id.region_id', store=True, readonly=True)
    territory_id = fields.Many2one('garden.territory', string='Ərazi', related='kran_id.territory_id', store=True, readonly=True)
    area_id = fields.Many2one('garden.area', string='Sahə', related='kran_id.area_id', store=True, readonly=True)
    rows = fields.Char(string='Cərgələr', related='kran_id.rows', store=True, readonly=True)

    state = fields.Selection([
        ('new', 'Yeni'),
        ('in_progress', 'İcrada'),
        ('done', 'Tamamlandı'),
        ('cancelled', 'Ləğv edildi')
    ], string='Status', default='new', tracking=True)

    create_date = fields.Datetime(
        string='Suvarmanın başlama tarixi', 
        default=fields.Datetime.now,
        readonly=True
    )
    end_date = fields.Datetime(
        string='Suvarmanın bitmə tarixi', 
    )

    duration = fields.Float(string='Müddət (saat)', compute='_compute_duration', store=True)

    @api.depends('create_date', 'end_date')
    def _compute_duration(self):
        """Suvarmaya başlama və bitmə saatı arasındakı fərqi hesablayır"""
        for record in self:
            if record.create_date and record.end_date:
                delta = record.end_date - record.create_date
                record.duration = delta.total_seconds() / 3600  # saata çevir
            else:
                record.duration = 0.0
            
    amount_of_water = fields.Float(string='Su miqdarı (litrlə)', required=True)
    land_size = fields.Float(string='Torpaq sahəsi (ha)', required=True)

    def action_mark_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_mark_done(self):
        if not self.end_date:
            self.end_date = fields.Datetime.now()
        self.write({'state': 'done'})

    def action_mark_cancelled(self):
        self.write({'state': 'cancelled'})