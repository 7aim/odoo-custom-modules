# -*- coding: utf-8 -*-
from odoo import models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_customer_due_amount(self):
        """Müştərinin ümumi debitor borcunu hesablayır."""
        self.ensure_one()
        domain = [
            ('partner_id', '=', self.id),
            ('account_id.account_type', '=', 'asset_receivable'),
            ('move_id.state', '=', 'posted'),
        ]
        account_move_lines = self.env['account.move.line'].search(domain)
        return sum(line.balance for line in account_move_lines)

    def _get_pos_ui_res_partner(self, params):
        """
        Bu, Odoo 18 üçün DÜZGÜN funksiyadır.
        POS-a göndərilən müştəri məlumatlarına köhnə borcu əlavə edir.
        """
        # Əvvəlcə Odoo-nun standart funksiyasını çağırıb müştəri məlumatlarını alırıq
        partners = super()._get_pos_ui_res_partner(params)
        
        # Hər bir müştəri üçün borcu hesablayıb nəticəyə əlavə edirik
        for partner_data in partners:
            partner_record = self.browse(partner_data['id'])
            partner_data['customer_old_due'] = partner_record._get_customer_due_amount()
            
        return partners