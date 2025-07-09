from odoo import models, fields, api

class PrintJob(models.Model):
    _name = 'pos.print.job'
    _description = 'Print Job'
    _order = 'create_date desc'

    name = fields.Char(string='Job Name', required=True)
    content = fields.Text(string='Print Content', required=True)
    content_type = fields.Selection([
        ('receipt', 'Receipt'),
        ('invoice', 'Invoice'),
        ('report', 'Report'),
        ('label', 'Label'),
        ('other', 'Other'),
    ], string='Content Type', default='receipt')

    status = fields.Selection([
        ('pending', 'Pending'),
        ('printed', 'Printed'),
    ], string='Status', default='pending')

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    def action_print_browser(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/print/job/{self.id}',
            'target': 'new',
        }
    
    def action_mark_printed(self):
        self.write({'status': 'printed'})
        return True