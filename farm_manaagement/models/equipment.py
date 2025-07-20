from odoo import fields,models,api,_

class FarmEquipment(models.Model):
	_name = 'equipment.equipment'
	_rec_name = 'equipment_name'

	sequence = fields.Char('Sequence',required=True,index=True,copy=False,default=lambda self:_('new'))
	equipment_name = fields.Char(string="Equipment Name",required=True)
	equipment_category = fields.Many2one('equipment.category',string="Equipment Category",required=True)
	company = fields.Many2one('res.company',string="Company",required=True)
	used_by = fields.Selection([('farm','Farm'),('vehicle','Vehicle')],string="Used By")
	maintenance_team = fields.Char(string="Maintenance Team")
	technician = fields.Char(string="Technician")
	used_in_location = fields.Char(string="Used in Location")
	work_center = fields.Char(string="Work Center")
	description = fields.Text(string="Description")
	employee_name = fields.Many2one('hr.employee',string="Employee")
	# employee_id = fields.One2many('hr.employee',string="Employee")
	department_name = fields.Many2one('hr.department',string="Job Type")

	@api.model
	def create(self,vals):
		if vals.get('sequence',_('new'))==_('new'):
			vals['sequence'] = self.env['ir.sequence'].next_by_code('equipment.equipment') or _('new')
		result = super(FarmEquipment,self).create(vals)
		return result

class EquipmentCategory(models.Model):
	_name = 'equipment.category'
	_rec_name = 'category_name'

	category_name = fields.Char(satring="Category Name",required=True)
	user_name = fields.Many2one('res.users',string="User Name")
	company = fields.Many2one('res.company',string="Company",required=True)







