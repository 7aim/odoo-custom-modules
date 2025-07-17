from odoo import models, fields, api

class GardenProblem(models.Model):
    _name = 'garden.problem'
    _description = 'Bağça Problemi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name' # Qeydlər bu adla tanınacaq

    # ----------- ƏSAS SAHƏLƏR -----------
    name = fields.Char(string='Başlıq', required=True)
    note = fields.Text(string='Qeyd')
    inspector_note = fields.Text(string='Yoxlayan Şəxs Qeyd')
    image = fields.Image(string='Şəkil')

    # ----------- YER MƏLUMATLARI -----------
    subregion_id = fields.Many2one('garden.subregion', string='Kiçik Bölgə')
    # Related fields - Kiçik Bölgə seçilən kimi avtomatik dolacaq
    region_id = fields.Many2one('garden.region', string='Bölgə', related='subregion_id.region_id', store=True)
    territory_id = fields.Many2one('garden.territory', string='Ərazi', related='subregion_id.territory_id', store=True)
    area_id = fields.Many2one('garden.area', string='Sahə', related='subregion_id.area_id', store=True)
    rows = fields.Char(string='Cərgələr')

    # ----------- İŞTİRAKÇILAR -----------
    executor_id = fields.Many2one('res.users', string='İcraçı')
    inspector_id = fields.Many2one('res.users', string='Problemi aşkarlayan', default=lambda self: self.env.user)

    # ----------- TƏSNİFAT -----------
    problem_type = fields.Selection(
        selection='_get_problem_types',
        string='Problem Növü'
    )
    priority = fields.Selection([
        ('0', 'Aşağı'), ('1', 'Normal'), ('2', 'Vacib'), ('3', 'Təcili')
    ], string='Prioritet Növü', default='0')

    # ----------- STATUS VƏ TARİX -----------
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
    deadline = fields.Date(string='Son İcra Tarixi')

    @api.model
    def _get_problem_types(self):
        return self.env['soraqca.panel'].get_selection_items('problem_novleri')
    
    # ----------- ACTION DÜYMƏLƏRİ -----------
    def action_mark_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_mark_done(self):
        self.write({'state': 'done'})

    def action_mark_cancelled(self):
        self.write({'state': 'cancelled'})

