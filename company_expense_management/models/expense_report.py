from odoo import models, fields, api

class ExpenseReport(models.Model):
    _name = 'company.expense.report'
    _description = 'Company Expense Report'

    name = fields.Char(string='Açıqlama', required=True)

    expense_line_ids = fields.One2many(
        comodel_name='company.expense.line',
        inverse_name='report_id',
        string='Xərc Sətirləri'
    )

    user_id = fields.Many2one(
        'res.users',
        string='İşçi',
        required=True,
        default=lambda self: self.env.user
    )

    state = fields.Selection([
        ('draft', 'Qaralama'),
        ('submitted', 'Təsdiqdə'),
        ('approved', 'Təsdiqləndi'),
        ('paid', 'Ödənildi'),
        ('rejected', 'Rədd Edildi'),
    ], string='Status', default='draft', readonly=True, copy=False)

    total_amount = fields.Monetary(
        string='Ümumi Məbləğ',
        compute='_compute_total_amount',
        store=True,
        currency_field='currency_id'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Valyuta',
        default=lambda self: self.env.company.currency_id
    )

    vendor_bill_id = fields.Many2one(
        'account.move', 
        string='Satıcı Fakturası', 
        readonly=True, 
        copy=False
    )

    @api.depends('expense_line_ids.amount')
    def _compute_total_amount(self):
        for report in self:
            total = 0.0
            for line in report.expense_line_ids:
                total += line.amount
            report.total_amount = total

    
    def action_submit(self):
        self.ensure_one()
        self.write({'state': 'submitted'})
        return True

    # köhnə action_approve metodunu silib bunu onun yerinə yazın
    def action_approve(self):
        self.ensure_one()

        # Faktura üçün sətirləri hazırlayırıq
        invoice_lines = []
        for line in self.expense_line_ids:
            invoice_lines.append((0, 0, {
                'name': line.description,
                'quantity': 1,
                'price_unit': line.amount,
                # !!! VACİB QEYD: Aşağıdakı account_id-ni öz sisteminizə uyğunlaşdırın
                'account_id': 69, # <-- BU RƏQƏMİ DƏYİŞİN
            }))

        # Fakturanı (Vendor Bill) yaradırıq
        vendor_bill = self.env['account.move'].create({
            'move_type': 'in_invoice', # Bu, Satıcı Fakturası (Vendor Bill) olduğunu bildirir
            'partner_id': self.user_id.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': invoice_lines,
        })

        # Yaradılmış fakturanı xərc hesabatımıza bağlayırıq və statusu dəyişirik
        self.write({
            'state': 'approved',
            'vendor_bill_id': vendor_bill.id,
        })
        return True

    def action_pay(self):
        self.ensure_one()
        self.write({'state': 'paid'})
        return True

    def action_reject(self):
        self.ensure_one()
        self.write({'state': 'rejected'})
        return True

    def action_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})
        return True

# ExpenseLine class-ı olduğu kimi qalır, orada dəyişiklik yoxdur
class ExpenseLine(models.Model):
    _name = 'company.expense.line'
    _description = 'Company Expense Line'

    report_id = fields.Many2one('company.expense.report', string='Xərc Hesabatı', ondelete='cascade')
    date = fields.Date(string='Tarix', required=True)
    description = fields.Char(string='Açıqlama', required=True)
    amount = fields.Monetary(string='Məbləğ', required=True, currency_field='currency_id')
    currency_id = fields.Many2one(related='report_id.currency_id', string='Valyuta')