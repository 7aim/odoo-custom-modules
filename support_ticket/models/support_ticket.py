from odoo import models, fields, api

class SupportTicket(models.Model):
    _name = 'support.ticket'
    _description = 'Support Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Ticket Nömrəsi', required=True, copy=False, readonly=True, default='Yeni')
    subject = fields.Char(string='Mövzu', required=True, tracking=True)
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

    @api.model
    def create(self, vals):
        """Ticket yaradıldıqda avtomatik nömrə ver və müştərini follower et"""
        if vals.get('name', 'Yeni') == 'Yeni':
            vals['name'] = self.env['ir.sequence'].next_by_code('support.ticket') or 'Yeni'
        
        result = super(SupportTicket, self).create(vals)
        
        # Müştərini avtomatik follower et
        if result.partner_id:
            result.message_subscribe(partner_ids=[result.partner_id.id])
        
        return result
    
    def action_start_work(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_solve(self):
        for rec in self:
            rec.state = 'solved'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'