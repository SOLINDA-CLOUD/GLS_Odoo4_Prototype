from odoo import _, api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    top = fields.Char('Terms Of Payment')
    delivery_time = fields.Char('Delivery Time')    
    notes = fields.Text('Notes')    
    price = fields.Float('Price/Frangko')