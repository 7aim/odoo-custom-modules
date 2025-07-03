# -*- coding: utf-8 -*-

from odoo import models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def export_for_printing(self):
        # Standart funksiyadan bütün məlumatları alırıq
        result = super(PosOrder, self).export_for_printing()

        # Sifarişə bağlı müştəri varsa
        partner = self.partner_id
        if partner:
            # Partnyorun debitor borclarını hesablamaq üçün
            # 'account.move.line'-dan istifadə edirik.
            # Bu, mühasibatlıqdakı bütün ödənilməmiş invoysları nəzərə alacaq.
            self.env.cr.execute("""
                SELECT SUM(aml.debit - aml.credit)
                FROM account_move_line aml
                JOIN account_account aa ON (aml.account_id = aa.id)
                WHERE aml.partner_id = %s
                AND aa.account_type = 'asset_receivable'
                AND aml.parent_state = 'posted'
            """, (partner.id,))
            partner_due = self.env.cr.fetchone()[0] or 0.0
            result['partner_due'] = partner_due
        else:
            result['partner_due'] = 0.0

        return result