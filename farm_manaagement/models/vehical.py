from odoo import fields,models,api

class Vehical(models.Model):

	_name = 'vehical.vehical'
	_description = 'Vehical Manage Form'

	license_plate = fields.Char('License Plate')
	vehicle_name = fields.Char(string="Vehical Name",required=True)
	model_name = fields.Char(string="Vehical Model",required=True)
	vehicle_number = fields.Char(string="Vehical Number")
	driver = fields.Char(string="Driver Name")
	fuel_type = fields.Char(string="Fuel Type")

# class VehicalDetails(models.Model):


