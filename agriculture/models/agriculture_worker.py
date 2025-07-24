# -*- coding: utf-8 -*-
from odoo import models, fields, api

# Kənd Təsərrüfatı İşçisi
class AgricultureWorker(models.Model):
    _name = 'agriculture.worker'
    _description = 'Kənd Təsərrüfatı İşçisi'
    _order = 'name'

    name = fields.Char(string="İşçi Adı", required=True)
    phone = fields.Char(string="Telefon")
    daily_wage = fields.Monetary(string="Günlük Maaş", currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', string="Valyuta", default=lambda self: self.env.company.currency_id)
    
    # Başlanğıc və bitiş tarixləri
    start_date = fields.Date(string="İşə Başlama Tarixi", default=fields.Date.context_today)
    end_date = fields.Date(string="İşdən Çıxma Tarixi")
    
    active = fields.Boolean(string="Aktiv", default=True)
    state = fields.Selection([
        ('active', 'Aktiv'),
        ('inactive', 'Qeyri-aktiv'),
        ('terminated', 'İşdən çıxarılmış')
    ], string="Status", default='active', required=True)
    
    # Hesabat sahələri
    total_operations = fields.Integer(string="Ümumi Əməliyyat Sayı", compute='_compute_stats', store=False)
    total_earnings = fields.Monetary(string="Ümumi Qazanc", compute='_compute_stats', store=False, currency_field='currency_id')
    total_payments = fields.Monetary(string="Ödənilmiş Məbləğ", compute='_compute_stats', store=False, currency_field='currency_id')
    balance = fields.Monetary(string="Balans (Qazanc - Ödəniş)", compute='_compute_stats', store=False, currency_field='currency_id')
    
    # Qeydlər
    notes = fields.Text(string="Qeydlər")

    @api.depends('daily_wage')
    def _compute_stats(self):
        """İşçi statistikalarını hesabla"""
        for worker in self:
            # Əməliyyat sayı və qazanc
            operations = self.env['agriculture.operation'].search([('worker_ids', 'in', worker.id), ('state', '=', 'done')])
            worker.total_operations = len(operations)
            worker.total_earnings = worker.total_operations * worker.daily_wage
            
            # Ödənilmiş məbləğ
            payments = self.env['agriculture.worker.payment'].search([('worker_id', '=', worker.id), ('state', '=', 'paid')])
            worker.total_payments = sum(payment.amount for payment in payments)
            
            # Balans
            worker.balance = worker.total_earnings - worker.total_payments

    def action_view_operations(self):
        """İşçinin əməliyyatlarını göstər"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.name} - Əməliyyatlar',
            'res_model': 'agriculture.operation',
            'view_mode': 'list,form',
            'domain': [('worker_ids', 'in', self.id)],
            'context': {'default_worker_ids': [(6, 0, [self.id])]},
        }

    def action_view_payments(self):
        """İşçinin ödənişlərini göstər"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.name} - Ödənişlər',
            'res_model': 'agriculture.worker.payment',
            'view_mode': 'list,form',
            'domain': [('worker_id', '=', self.id)],
            'context': {'default_worker_id': self.id},
        }


class AgricultureWorkerPayment(models.Model):
    _name = 'agriculture.worker.payment'
    _description = 'İşçi Ödənişi'
    _order = 'date desc, id desc'

    name = fields.Char(string="Ödəniş", compute='_compute_name', store=True)
    worker_id = fields.Many2one('agriculture.worker', string="İşçi", required=True, ondelete='cascade')
    date = fields.Date(string="Ödəniş Tarixi", required=True, default=fields.Date.context_today)
    amount = fields.Monetary(string="Məbləğ", required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Valyuta", default=lambda self: self.env.company.currency_id)
    
    payment_type = fields.Selection([
        ('salary', 'Maaş'),
        ('bonus', 'Bonus'),
        ('advance', 'Avans'),
        ('other', 'Digər')
    ], string="Ödəniş Növü", default='salary', required=True)
    
    description = fields.Text(string="Açıqlama")
    
    # Status
    state = fields.Selection([
        ('draft', 'Qaralama'),
        ('paid', 'Ödənilmiş'),
        ('cancelled', 'Ləğv edilmiş')
    ], string="Status", default='draft', required=True)

    @api.depends('worker_id', 'date', 'amount')
    def _compute_name(self):
        for payment in self:
            if payment.worker_id and payment.date:
                payment.name = f"{payment.worker_id.name} - {payment.date.strftime('%Y-%m-%d')} - {payment.amount} AZN"
            else:
                payment.name = "Yeni Ödəniş"

    def action_confirm_payment(self):
        """Ödənişi təsdiqlə"""
        self.write({'state': 'paid'})

    def action_cancel_payment(self):
        """Ödənişi ləğv et"""
        self.write({'state': 'cancelled'})

    def action_draft_payment(self):
        """Ödənişi qaralama vəziyyətinə qaytar"""
        self.write({'state': 'draft'})
