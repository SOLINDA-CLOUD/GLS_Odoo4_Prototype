from odoo import _, api, fields, models

class BusinessType(models.Model):
    _name = 'business.type'
    _description = 'Business Type'
    
    name = fields.Char('Business Name')

class WastewaterType(models.Model):
    _name = 'wastewater.type'
    _description = 'Type Wastewater for Tertiary Treatment'
    
    name = fields.Char('name')

class TransportSurvey(models.Model):
    _name = 'transport.survey'
    _description = 'Transport Survey'
    
    name = fields.Char('name')

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    business_type_id = fields.Many2one('business.type', string='Business Type')

    ground_water = fields.Boolean('Ground Water')
    surface_water = fields.Selection([
        ('river', 'River'),
        ('lake', 'Lake or reservoir'),
    ], string='Surface Water')
    seawater = fields.Selection([
        ('intake', 'Open intake'),
        ('beach', 'Beach well'),
    ], string='Seawater')
    waste_water_treatment = fields.Selection([
        ('municipal', 'Municipal'),
        ('domestic', 'Domestic'),
        ('industrial', 'Industrial'),
    ], string='Wastewater for Tertiary Treatment')
    distance_from_rawwater = fields.Char('Distance from Raw Water Source to Treatment Plant')
    elevation_from_rawwater = fields.Char('Elevation from Raw Water Source to Treatment Plant')
    #What are the dimensions of the availabl space for the treatment plant?
    length_treatment_plant = fields.Float('Length')
    width_treatment_plant = fields.Float('Width')
    height_treatment_plant = fields.Float('Height')
    gradient_treatment_plant = fields.Float('Gradient')
    
    wind_load = fields.Char('What is the specified wind load?')
    specific_governmental = fields.Boolean('Are there specific governmental standards')
    specific_material = fields.Boolean('Are there specific materials preferred for construction?')
    any_data_available = fields.Boolean('Are there any data available regarding the soil composition, ground water level, etc.?')
    flange_type = fields.Selection([
        ('din', 'DIN'),
        ('ansi', 'ANSI'),
        ('jis', 'JIS')
    ], string='Which flange types are required?')
    is_seasonal_deviations = fields.Boolean('Are there seasonal deviations within the production process(es)?')
    is_height_limitation = fields.Boolean('Are there height limitation?')
    is_area_limitation = fields.Boolean('Are there area limitations?')
    is_limitation_to_transport_tanks = fields.Boolean('Are there any limitations to transport tanks, orreactors, from GLS  to the customer.')
    transport_id = fields.Many2one('transport.survey', string='Transport by')
    # Electrical Condition On Location

    voltage = fields.Float('What is the available voltage?')
    frequency = fields.Float('What is the available frequency?')
    available_power = fields.Float('What is the available power?')
    power = fields.Float('Distance between power supply and treatment plant')
    source_power = fields.Selection([
        ('pln', 'PLN'),
        ('own', 'Own Power Plant')
    ], string='Source of power supply')

    # Description of the Area
    description_area = fields.Html('Description of the Area')
    is_attachment = fields.Boolean('Drawings available?')
    attachment_area = fields.Binary('Attachment Area')

    # Additional Remarks or Documentations (Pictures, Sketches)

    description_remarks = fields.Html('Additional Remarks or Documentations (Pictures, Sketches)')
    attachment_remarks = fields.Binary('Attachment')











