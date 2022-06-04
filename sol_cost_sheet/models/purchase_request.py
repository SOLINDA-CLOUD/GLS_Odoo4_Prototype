from odoo import _, api, fields, models

class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'
    
    item_id = fields.Many2one('item.item', string='Item')    