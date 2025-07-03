# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Bu funksiya müştərinin ümumi borcunu hesablayır
    def _get_customer_due_amount(self):
        self.ensure_one()
        # Yalnız 'receivable' (debitor) tipli hesablardakı borclara baxırıq
        domain = [
            ('partner_id', '=', self.id),
            ('account_id.account_type', '=', 'asset_receivable'),
            ('move_id.state', '=', 'posted'),
        ]
        # Bütün uyğun qeydləri tapırıq
        account_move_lines = self.env['account.move.line'].search(domain)
        # Balansı cəmləyirik
        return sum(line.balance for line in account_move_lines)

    # Bu funksiya Odoo-nun standart funksiyasını genişləndirərək POS-a əlavə məlumat ötürür
    def _get_pos_ui_pos_order_ui_data_by_partner(self):
        # Orijinal funksiyanın nəticəsini alırıq
        data = super()._get_pos_ui_pos_order_ui_data_by_partner()
        # Öz məlumatımızı əlavə edirik
        data['customer_old_due'] = self._get_customer_due_amount()
        return data