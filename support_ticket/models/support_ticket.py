from odoo import models, fields

class SupportTicket(models.Model):
    _name = 'support.ticket'
    _description = 'Support Ticket'
    # Chatter funksionallığı (tarixçə, mesajlar) üçün bu iki modeli irs alırıq
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Mövzu', required=True, tracking=True)
    description = fields.Text(string='Açıqlama', tracking=True)
    
    state = fields.Selection([
        ('new', 'Yeni'),
        ('in_progress', 'İcra Edilir'),
        ('solved', 'Həll Edildi'),
        ('cancelled', 'Ləğv Edildi')
    ], string='Status', default='new', tracking=True)

    priority = fields.Selection([
        ('0', 'Aşağı'),
        ('1', 'Normal'),
        ('2', 'Yüksək')
    ], string='Prioritet', default='1', tracking=True)

    # 'res.partner' Odoo-nun standart "Contacts" modelidir
    partner_id = fields.Many2one('res.partner', string='Müştəri', required=True, tracking=True)
    
    # 'res.users' Odoo-nun standart "Users" modelidir
    user_id = fields.Many2one('res.users', string='Agent', default=lambda self: self.env.user, tracking=True)