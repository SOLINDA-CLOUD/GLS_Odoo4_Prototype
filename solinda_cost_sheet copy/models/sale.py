from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # rab_id = fields.Many2one('cost.sheet',compute='_compute_rab_id', string='RAB', store=True)
    rab_id = fields.Many2one('cost.sheet',related='opportunity_id.rab_id', string='RAB', store=True)
    
