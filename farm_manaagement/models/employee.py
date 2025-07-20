from odoo import models, fields, api, _


# class EmployeeEmployee(models.Model):
# 	_inherit = 'hr.employee'

# 	type_id = fields.Many2one('employee.type',string="Type")
# 	location = fields.Many2one('agriculture.agriculture',string="Location")

class EmployeeType(models.Model):
    _name = 'employee.type'
    _rec_name = "name"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    age = fields.Date(string="Age")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    photo = fields.Binary(string="Image")
    email = fields.Char(string="Email")
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State')


class AgricultureAgriculture(models.Model):
    _name = 'agriculture.agriculture'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "owner_name"

    owner_name = fields.Many2one('hr.employee', string="Name", required=True)
    owner_type = fields.Many2one('employee.type', string='Owner Type')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    zip = fields.Char(string='Zip')
    priority = fields.Selection([('low', 'Low'), ('medium', 'Midium'), ('high', 'High'), ('very high', 'Very High')])
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', string='State')
    agree_land = fields.Float(string="Land")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile", required=True)
    # type = fields.Many2one('employee.type',string="Type")
    photo = fields.Binary(string="Image", related='owner_name.image_1920')
    email = fields.Char(string="Email", required=True)
    farm_land_ids = fields.One2many('farm.land.line', 'farm_id', string="Farm Land")
    crop_history_ids = fields.One2many('farm.crop.line', 'crop_id', string="Crop History")
    user_company = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.id)
    # location=fields.One2many('location.location','c',string="nowpass")
    user_id = fields.Many2one('res.users', string="User")
    color = fields.Integer('Color Index', default=0)

    @api.onchange('country_id')
    def onchange_nationality(self):
        domain = {'state_id': [('country_id', '=', self.country_id.id)]}
        return {'domain': domain}

# @api.onchange("owner_name")
# def onchange_owner_type(self):
# 	print("-------->",self)
# 	if self.owner_name:
# 		self.owner_type = self.owner_name.type_id


class FarmLand(models.Model):
    _name = 'farm.land.line'
    _rec_name = "location"

    owner_name = fields.Many2one('farm.location', string="Owner Name")
    location_connect = fields.Many2one("location.location", string="Location")
    location = fields.Many2one('location.location', string="Location")
    acre = fields.Float(string="Acre")
    # acre = fields.Float(string="Acre")
    # location = fields.Char(string="Location",related="owner_name.location")
    # location = fields.Char(string="Location")
    worker = fields.Many2many('hr.employee', string="Worker")
    crop = fields.Many2one("crop.crop", string="Crop")
    year = fields.Date(string="Year")
    location_state = fields.One2many('location.location', 'c', string="nowpass")
    farm_id = fields.Many2one('agriculture.agriculture', string="Farming")

    @api.onchange("acre")
    def onchange_sub_client(self):
        print("-------->", self)
        if self.location:
            self.location.acre = self.acre


class FarmCrop(models.Model):
    _name = 'farm.crop.line'
    _rec_name = "location_id"

    location_id = fields.Many2one('location.location', string="Location")
    # location_id = fields.Many2one('farm.land.line',string="Location_id")
    owner_name = fields.Many2one('farm.location', string="Owner Name")
    # location=fields.Many2one('location.location',string="location")
    crop = fields.Char(string="Crop")
    year = fields.Date(string="Year")
    crop_id = fields.Many2one('agriculture.agriculture', string="Crop")
    location = fields.Char(string="Location")
    acre = fields.Float(string="Acre")


class FarmLocation(models.Model):
    _name = 'farm.location'
    _rec_name = "o"
    owner_name = fields.Many2one('hr.employee', string="Owner", required=True)
    o = fields.Many2one("location.location")
    total_acre = fields.Char(string="Total Acre")
    loc = fields.Char(string="Location")
    location = fields.One2many('location.location', 'connected_field', string="Location")


class Location(models.Model):
    _name = "location.location"
    _rec_name = "location"
    _desciption = "Information about Location"

    connected_field = fields.Many2one('farm.location', string="Location")
    c = fields.Many2one('farm.land.line', string="passvalue")
    location = fields.Char(string="Location")
    acre = fields.Float(string="Acre")


class ProductTemplate(models.Model):
    _inherit = 'product.template'


class FarmCrop(models.Model):
    _name = "farm.crop.config"
    _rec_name = "season_name_conf"

    crop_name_id_conf = fields.Many2many('product.template', string="Crop Name")
    season_name_conf = fields.Selection([('summer', 'Summer'), ('winter', 'Winter'), ('monson', 'Monson')],
                                        string="Season Name")


class CroppingSeasons(models.Model):
    _name = 'cropping.seasons.line'
    _rec_name = "kharif"

    kharif = fields.Selection([('rice', 'Rice'), ('cotton', 'Cotton'), ('soybean', 'Soybean'), ('jowar', 'Jowar')],
                              string="Kharif")
    rabi = fields.Selection([('wheat', 'Wheat'), ('bajra', 'Bajra'), ('gram', 'Gram'), ('mustard', 'Mustard')],
                            string="Rabi")
    zaid = fields.Selection([('cucumber', 'Cucumber'), ('pumpkin', 'Pumpkin'), ('pulse', 'Pulse')], string="Zaid")


class AddKanban(models.Model):
    _name = 'add.kanban'
    _description = 'Add Kanban In Bottom'

    owner_name = fields.Many2one('hr.employee', string="Name", required=True)
    phone = fields.Char(string="Phone")
    country_id = fields.Many2one('res.country', string='Country', required=True)
    email = fields.Char(string="Email", required=True)
