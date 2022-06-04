from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'
    
    payment_schedule_line_ids = fields.One2many('payment.schedule', 'order_id', string='Payment Schedule Line')
    
    
    @api.onchange('payment_schedule_line_ids')
    def _onchange_payment_schedule_line_ids(self):
        total = sum(self.payment_schedule_line_ids.mapped('total_amount'))
        if total > self.amount_total:
            raise ValidationError("Total in Payment Schedule is greater then total amount in sales")
    
class PaymentSchedule(models.Model):
    _name = 'payment.schedule'
    _description = 'Payment Schedule'
    
    order_id = fields.Many2one('sale.order', string='Sale Order')    
    payment_date = fields.Date('Payment Date')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    amount = fields.Monetary(currency_field='currency_id')
    # product_id = fields.Many2one('product.product', string='Service')
    account_id = fields.Many2one('account.account', string='Account')
    name = fields.Char('Description')
    progress = fields.Float('Progress')
    bill = fields.Float('Bill')
    
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount')
    
    
    @api.depends('order_id.amount_total','bill')
    def _compute_total_amount(self):
        for this in self:
            this.total_amount = this.bill * this.order_id.amount_total
    
    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id:
    #         self.name = self.product_id.display_name
    #     else:
    #         self.name = False
    

    def create_invoice(self):
        invoice_vals = self.order_id._prepare_invoice()
        invoice_vals['invoice_line_ids'] = [(0,0,{
            'sequence': 10,
            'name': self.name,
            # 'product_id': self.product_id.id,
            # 'product_uom_id': self.product_id.uom_id.id,
            'account_id': self.account_id.id,
            'quantity': 1,
            'price_unit': self.total_amount,
            'analytic_account_id': self.order_id.analytic_account_id.id,
            # 'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)]
        })]
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)
        return {
                        'name': '%s - %s'%(self.order_id.name,self.name),
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'account.move',
                        'res_id': moves.id,
            
        }
             
    @api.constrains('amount')
    def _constrains_amount(self):
        for this in self:
            total = this.order_id.amount_total
            if this.amount > total:
                raise ValidationError('Amount field is greater then sales total amount')
    
    # @api.onchange('payment_term_id')
    # def _onchange_payment_term_id(self):
    #     if self.payment_term_id:
    #         days = self.payment_term_id.line_ids[0].days
    #         self.payment_date = self.order_id.date_order + relativedelta(days=days)
    #     else:
    #         self.payment_date = False