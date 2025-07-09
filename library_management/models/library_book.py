from odoo import models, fields, api
from datetime import timedelta

class LibraryBook(models.Model):
    _name = 'library.book' 
    _description = 'Library Book'  

    name = fields.Char(string='Title', required=True)
    isbn = fields.Char(string='ISBN')
    active = fields.Boolean(string='Active?', default=True)
    description = fields.Text(string='Description')

    author_id = fields.Many2one('library.author', string='Author')
    category_ids = fields.Many2many('library.book.category', string='Categories')
    
    borrow_date = fields.Date(string='Borrow Date', readonly=True)
    due_date = fields.Date(string='Due Date', compute='_compute_due_date', readonly=True)

    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')

    state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
    ], string='Status', default='available', required=True)

    @api.depends('borrow_date')
    def _compute_due_date(self):
        for book in self:
            if book.borrow_date:
                book.due_date = book.borrow_date + timedelta(days=7)
            else:
                book.due_date = False 

    @api.onchange('author_id')
    def _onchange_author(self):
        if self.author_id and self.author_id.birth_date:
            return {
                'warning': {
                    'title': "Məlumat",
                    'message': f"Seçdiyiniz yazıçı ({self.author_id.name}) {self.author_id.birth_date}-ci il təvəllüdlüdür.",
                }
            }

    def make_borrowed(self):
        self.write({
            'state': 'borrowed',
            'borrow_date': fields.Date.today() 
        })

    def make_available(self):
        self.write({
            'state': 'available',
            'borrow_date': False 
        })

    # Eyni anda bir nece qeydi yarada biler
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('library.book') or 'New'
        return super().create(vals_list)