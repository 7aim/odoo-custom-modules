# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # 1. Yeni, hesablanan bir sahə yaradırıq
    customer_old_due = fields.Float(
        compute='_compute_customer_old_due',
        string="Köhnə Borc (POS üçün)"
    )

    # 2. Bu sahənin dəyərini hesablayan funksiya
    def _compute_customer_old_due(self):
        for partner in self:
            domain = [
                ('partner_id', '=', partner.id),
                ('account_id.account_type', '=', 'asset_receivable'),
                ('move_id.state', '=', 'posted'),
            ]
            account_move_lines = self.env['account.move.line'].search(domain)
            partner.customer_old_due = sum(line.balance for line in account_move_lines)