from odoo import _, api, fields, models

from odoo.exceptions import ValidationError

class Item(models.Model):
    _name = 'item.item'
    _description = 'Item'
    _rec_name = "product_id"
    
    
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet',ondelete="cascade")
    rap_id = fields.Many2one('rap.rap', string='RAP')
    product_id = fields.Many2one('product.product',required=True)
    category_id = fields.Many2one('rab.category', string='Category',ondelete="cascade")
    rap_category_id = fields.Many2one('rap.category', string='Category',ondelete="cascade")
    component_id = fields.Many2one('component.component',ondelete="cascade")
    product_type = fields.Selection(related='product_id.detailed_type',store=True)
    qty_on_hand = fields.Float('Qty On Hand',related='product_id.qty_available')
    
    product_qty = fields.Integer('Quantity',default=1)
    existing_price = fields.Float('Existing Price')
    rfq_price = fields.Float('RFQ Price')
    total_price = fields.Float(compute='_compute_total_price', string='Total Price',store=True)
    remarks = fields.Text('Remarks')
    created_after_approve = fields.Boolean('Created After Approve')
    can_be_purchased = fields.Boolean(compute='_compute_can_be_purchased', string='Can BE Purchased',store=True)
    rap_price = fields.Float('Price',default=lambda self:self.total_price)
    purchase_line_ids = fields.One2many('purchase.request.line', 'item_id', string='Purchase Line')
    
    @api.depends('qty_on_hand','product_qty')
    def _compute_can_be_purchased(self):
        for this in self:
            this.can_be_purchased = this.qty_on_hand < this.product_qty
        
    @api.depends('product_qty','rfq_price')
    def _compute_total_price(self):
        for this in self:
            this.total_price = this.product_qty * this.rfq_price
    
    @api.constrains('product_id')
    def _constrains_product_id(self):
        for this in self:
            data = this.env['item.item'].search([('cost_sheet_id', '=', this.cost_sheet_id.id),('category_id', '=', this.category_id.id),('product_id', '=', this.product_id.id)])
            if len(data) > 1:
                raise ValidationError('Cannot create same product in one item')

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id or self.component_id:
            self.cost_sheet_id = self.category_id.cost_sheet_id.id or self.component_id.cost_sheet_id.id
    
    
    def view_item_in_purchase(self):
        return {
                'name': 'Item In Purchase',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'purchase.request',
                'domain': [('id','in',self.purchase_line_ids.mapped('request_id.id'))],
                # 'res_id': purchase.id,
        }
    
    def create_purchase_request(self):
        # product_type = self.mapped('product_type')
        # if "service" in product_type or 'consu' in product_type:
        #     raise ValidationError("""There are a products with Product Type "Service" or "Consumable". Only "Storable Product" that can be create a Purchase Request """)
        items = [item.product_id.name for item in self if not item.can_be_purchased] # Pengecekan product/item yang tidak dapat create purchase karna qty_on_hand lebih atau sama dengan quantity  
        if items:
            raise ValidationError("""There are Product can't created purchase order because Qty on Hand is bigger or equal than Quantity:
            %s"""%items)
        
        purchase = self.env['purchase.request'].create({
            'line_ids':[(0,0,{
                'product_id': item.product_id.id,
                'product_qty': item.product_qty,
                'estimated_cost': item.rap_price,
                'item_id': item.id                
            }) for item in self]
        })
        
        return {
                'name': 'Purchase Request',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'purchase.request',
                'domain': [('id','=',purchase.id)],
                'res_id': purchase.id,
        }
