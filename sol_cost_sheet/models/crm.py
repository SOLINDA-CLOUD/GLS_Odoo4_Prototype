from odoo import _, api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    rab_id = fields.Many2one('cost.sheet', string='RAB')
    