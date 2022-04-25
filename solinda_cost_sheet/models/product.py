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
    ], string='Product Group')    