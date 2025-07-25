from odoo import models, fields, api

class GardenProblem(models.Model):
    _name = 'garden.problem'
    _description = 'Bağça Problemi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Başlıq', required=True)
    note = fields.Text(string='Qeyd')
    inspector_note = fields.Text(string='Yoxlayan Şəxs Qeyd')
    image = fields.Image(string='Şəkil')

    subregion_id = fields.Many2one('garden.subregion', string='Kiçik Bölgə', required=True)
    region_id = fields.Many2one('garden.region', string='Bölgə', related='subregion_id.region_id', store=True)
    territory_id = fields.Many2one('garden.territory', string='Ərazi', related='subregion_id.territory_id', store=True)
    area_id = fields.Many2one('garden.area', string='Sahə', related='subregion_id.area_id', store=True)
    rows = fields.Char(string='Cərgələr')

    executor_id = fields.Many2one('hr.employee', string='İcraçı')
    inspector_id = fields.Many2one('hr.employee', string='Problemi aşkarlayan', required=True)

    problem_type = fields.Selection(
        selection='_get_problem_types',
        string='Problem Növü', required=True
    )
    priority = fields.Selection([
        ('0', 'Aşağı'), ('1', 'Normal'), ('2', 'Vacib'), ('3', 'Təcili')
    ], string='Prioritet Növü', default='0')

    state = fields.Selection([
        ('new', 'Yeni'),
        ('in_progress', 'İcrada'),
        ('done', 'Tamamlandı'),
        ('cancelled', 'Ləğv edildi')
    ], string='Status', default='new', tracking=True)
    create_date = fields.Datetime(
        string='Yaradılma Tarixi', 
        default=fields.Datetime.now,
        readonly=True
    )
    end_date = fields.Datetime(
        string='Bitmə Tarixi', 
    )
    deadline = fields.Datetime(string='Son İcra Tarixi', required=True)

    @api.model
    def _get_problem_types(self):
        return self.env['soraqca.panel'].get_selection_items('problem_novleri')
    
    def action_mark_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_mark_done(self):
        if not self.end_date:
            self.end_date = fields.Datetime.now()
        self.write({'state': 'done'})

    def action_mark_cancelled(self):
        self.write({'state': 'cancelled'})

