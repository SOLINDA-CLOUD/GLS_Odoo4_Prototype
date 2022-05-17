from odoo import _, api, fields, models

# class ProductProduct(models.Model):
#     _inherit = 'product.product'
    
#     product_group = fields.Selection([
#         ('general_work', 'General Work'),
#         ('intake_package', 'Intake Package'),
#         ('pretreatment_package', 'Pretreatment Package'),
#         ('swro_package', 'SWRO Package'),
#         ('brine_injection_package', 'Brine Injection Package'),
#         ('product_package', 'Product Package'),
#         ('electrical_package', 'Electrical Package'),
#         ('civil_work', 'Civil Work'),
#         ('ga_project', 'GA Project'),
#         ('waranty', 'Waranty'),
#     ], string='Product Group')    

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    product_group = fields.Selection([
        ('general_work', 'General Work'),
        ('intake_package', 'Intake Package'),
        ('pretreatment_package', 'Pretreatment Package'),
        ('swro_package', 'SWRO Package'),
        ('brine_injection_package', 'Brine Injection Package'),
        ('product_package', 'Product Package'),
        ('electrical_package', 'Electrical Package'),
        ('civil_work', 'Civil Work'),
        ('ga_project', 'GA Project'),
        ('waranty', 'Waranty'),
        ('ion_exchange', 'Ion Exchange Package'),
        ('media_filter', 'Media Filter Package'),
        ('carbon_filter', 'Carbon Filter Package'),
        ('softener', 'Softener Package'),
        ('electrode-ionization', 'Electrode-Ionization Package'),
        ('product_tank', 'Product Tank Package'),
        ('demin_tank', 'Demin Tank Package'),
        ('brine', 'Brine Package'),
        ('sludge_dewatering', 'Sludge Dewatering Package'),
        ('interconnecting', 'Interconnecting Package'),
        ('major_pumps', 'Major Pumps Package'),
        ('uv', 'Uv Package'),
        ('chemical', 'Chemical Package'),
        ('cip', 'Cip Package'),
        ('installation', 'Installation Package'),
        ('test_commissioning', 'Test Commissioning Package'),
        ('cation_exchange', 'Cation Exchange Package'),
        ('anion_exchange', 'Anion Exchange Package'),
        ('civil_construction', 'Civil Construction Package'),
        ('fbr', 'Fbr Package'),
        ('other1', 'Other1 Package'),
        ('other2', 'Other2 Package'),
        ('other3', 'Other3 Package'),
        ('other4', 'Other4 Package'),
        ('other5', 'Other5 Package'),

    ], string='Product Group')    