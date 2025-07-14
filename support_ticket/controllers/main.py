from odoo import http
from odoo.http import request

class SupportTicketController(http.Controller):

    @http.route('/support', type='http', auth='public', website=True)
    def support_form(self, **kwargs):
        return request.render('support_ticket.support_ticket_form_template', {})

    @http.route('/support/submit', type='http', auth='public', website=True, methods=['POST'])
    def support_form_submit(self, **post):
        request.env['support.ticket'].sudo().create({
            'partner_id': request.env['res.partner'].sudo().search([('email', '=', post.get('email'))], limit=1).id,
            'subject': f"{post.get('your_name')} tərəfindən müraciət", 
            'description': post.get('description'),
        })
        return request.render('support_ticket.support_ticket_thank_you_template', {})