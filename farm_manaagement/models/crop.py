from odoo import fields, models, api, _
# from datetime import datetime
# from datetime import datetime, date
import datetime


# import datetime as dt

# class ProductTemplate(models.Model):

# 	_inherit = "product.template"
# 	season = fields.Selection([('spring','Spring'),('summer','Summer'),('Autumn','Sutumn'),('winter','Winter')])


class Crop(models.Model):
    _name = "crop.crop"
    _description = "Crope Details"
    _rec_name = "owner_name"

    sequence = fields.Char('Sequence', required=True, index=True, copy=False, default=lambda self:_('new'))
    seq = fields.Char('Sequence',required=True,index=True,copy=False,default=lambda self:_('new'))
    crop_name = fields.Many2many('product.product', string="Crop Name", required=True)
    land_Of_hectore = fields.Float(string="Land Of Hectore")
    owner_name = fields.Char(string="Owner Name", required=True)
    location = fields.Selection([('porbandar', 'Porbandar'), ('junagadha', 'Junagadha'), ('ahemdabad', 'Ahemdabad')])
    worker_name = fields.Many2one('hr.employee', string="Worker Name")
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    crop_ids = fields.One2many('crop.name.line', 'crop_line_id', string="Crop Name")
    season_name = fields.Many2one('farm.crop.config', string="Season Name", required=True)
    period_to_produce = fields.Char(string="Period To Produce", compute="_compute_months")
    amount_untaxed = fields.Float(string="Untaxed Amount", compute='_amount_all')
    amount_tax = fields.Float(string="Taxes", compute='_amount_all')
    amount_total = fields.Float(string="Total", compute='_amount_all')
    note = fields.Text(string="Note")
    remaining = fields.Datetime(string="Remaining")
    produce = fields.Float(string="Produce")
    sedule_id = fields.One2many('sedule.sedule', 'sedule_line_id', string="Seduler")
    # Pesticides_medicine = fields.Char(string="Pesticides Medicine")
    # user_company=fields.Many2one('res.company',string="Company",default=lambda self:self.env.user.id)
    state = fields.Selection([('draft', 'Draft'), ('in progress', 'In Progress'), ('finished', 'Finished')],
                             string="State")

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'in progress'

    def action_finish(self):
        self.state = 'finished'

    @api.depends('crop_ids.total_price')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.crop_ids:
                amount_untaxed += line.total_price
            # amount_tax += line.tax_id
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed
            })

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('new')) == _('new'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('crop.crop') or _('new')
        result = super(Crop, self).create(vals)
        return result

    def _compute_months(self):
        if self.start_date and self.end_date:
            for rec in self:
                s_date = rec.start_date
                e_date = rec.end_date
                rec.period_to_produce = str((e_date - s_date).days) + " " + "Days"


class CropeName(models.Model):
    _name = "crop.name"
    _description = "Crope Name"

    crop_name = fields.Char(string="Crop Name")


class CropNameLine(models.Model):
    _name = "crop.name.line"
    _description = "Crop Name Line"

    # crop_name = fields.Many2one('crop.crop',string="Crop")
    crop = fields.Many2one('product.product', string="Crop")
    worker_name = fields.Many2many('hr.employee', string="Worker Name")
    expense_date = fields.Date(string="Expense Date")
    expense_name = fields.Many2one('hr.expense', string="Expenses Name")
    product_uom = fields.Many2one('uom.uom', string="Uom")
    product_uom_qty = fields.Float(string="Quantity")
    # quantity = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Unit Price")
    total_price = fields.Float(string="Subtotal")
    crop_line_id = fields.Many2one('crop.crop', string="Farming")
    tax_id = fields.Many2one('account.tax', string="Taxes")

    @api.onchange('product_uom_qty', 'price_unit', 'total_price')
    def _onchange_amount(self):
        for line in self:
            line.total_price = (line.price_unit) * (line.product_uom_qty)


class Seduler(models.Model):
    _name = "sedule.sedule"
    _description = "Sedule For The Task"

    sedule_line_id = fields.Many2one('crop.crop', string="Farming")
    worker_name = fields.Many2many('hr.employee', string="Worker Name")
    task_date = fields.Datetime(string="Task Date")
    task_name = fields.Char(string="Task Name")

    # user_company=fields.Many2one('res.company',string="Company",default=lambda self:self.env.user.id)

    # def _auto_mail_send (self):

    # 	tmpl_obj = self.pool.get ('email.template')
    # 	tmpl_ids = tmpl_obj.search (cr, uid, [('name', '=', 'Sedule Template Email')])
    # 	if tmpl_ids:
    # 		 tmpl_obj.write (cr, uid, tmpl_ids [0], {'email_to': email_to}, context = context)
    # 		 self.pool.get ('email.template'). Send_mail (cr, uid, tmpl_ids [0], obj.id)
    # 	return {}

    def worker_task_name(self):
        for task in self:
            # Send custom email template to leave applicant
            template = self.env.ref('farm_manaagement.crop_email_template')
            print("====================>", template)
            template.send_mail(task.id, force_send=True)
            # print("===============>",template)
            # Set leave status to Approved
            task.write({'state': 'finished'})
