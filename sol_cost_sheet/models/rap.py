from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round


class CsRAP(models.Model):
    _name = 'rap.rap'
    _description = 'RAP'
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name',tracking=True)
    crm_id = fields.Many2one('crm.lead', string='CRM',tracking=True)
    project_id = fields.Many2one('project.project', string='Project')
    date_document = fields.Date('Request Date',tracking=True,default=fields.Date.today)
    user_id = fields.Many2one('res.users', string='Responsible',default=lambda self:self.env.user.id)
    note = fields.Text('Term and condition')
    # approval_id = fields.Many2one('approval.approval', string='Approval')
    # approver_id = fields.Many2one('approver.line', string='Approver')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approve_gm', 'Waiting Approval GM'),
        ('waiting_approve_dir', 'Waiting Approval Direksi'),
        ('done', 'Done'),
        ('revisied', 'Revisied'),
        ('cancel', 'Canceled'),
    ], string='Status',tracking=True, default="draft")
    category_line_ids = fields.One2many('rap.category', 'rap_id', string='Category Line')
    

    currency_id = fields.Many2one('res.currency', string='currency',default=lambda self:self.env.company.currency_id.id)
    # is_approver = fields.Boolean(compute='_compute_is_approver', string='Is Approver')
    
    @api.model
    def create(self, vals):
        res = super(CsRAP, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("rap.rap")
        # res.crm_id.rab_id = res.id
        return res 
    
    def action_submit(self):
        self.write({'state':'waiting_approve_gm'})
    def action_approve_gm(self):
        self.write({'state':'waiting_approve_dir'})
    def action_approve_dir(self):
        self.write({'state':'done'})
    def action_to_draft(self):
        self.write({'state':'draft'})
    def action_cancel(self):
        self.write({'state':'cancel'})
    def action_revision(self):
        self.write({'state':'revisied'})
        

    
    def view_component_rap(self):
        return {
                'name': 'Component RAP',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'item.item',
                'view_id' : self.env.ref('sol_cost_sheet.rap_component_view_tree').id,
                'domain': [('rap_id','=',self.id)]
                # 'domain': [('rap_id','=',self.id),('can_be_purchased','=',True)]
        }
    
    @api.model
    def create(self, vals):
        res = super(CsRAP, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("rap.rap")
        # res.crm_id.rab_id = res.id
        return res 
    
    # @api.depends('approver_id','approval_id')
    # def _compute_is_approver(self):
    #     for this in self:
    #         if this.approval_id or this.approver_id:
    #             if this.approval_id.approval_type == 'user':
    #                 this.is_approver = this.env.user.id in this.approver_id.user_ids.ids
    #             else:
    #                 this.is_approver = this.env.user.id in this.approver_id.group_ids.users.ids
    #         else:
    #             this.is_approver = False

    def waiting_approval(self):
        for request in self:
            request.approval_id = request.env['approval.approval'].search([('active', '=', True)],limit=1)
            if bool(request.approver_id):
                approver_id = request.approval_id.approver_line_ids.search([("amount", "<=", request.total_amount),('sequence','>',request.approver_id.sequence)],limit=1)
                if approver_id:
                    request.write({"approver_id": approver_id.id})
                    # request.notify()
                else:
                    request.write({"state": "done","approver_id":False })

            else:
                approver_id = request.approval_id.approver_line_ids.search([("amount", "<=", request.total_amount)],order="sequence ASC",limit=1)
                if approver_id:
                    request.write(
                        {
                            "approver_id": approver_id.id,
                            "state": "waiting",
                        }
                    )
                    # request.notify()
                else:
                    request.write(
                        {
                            "state": "done",
                            "approver_id":False
                        }
                    )
                    

    def action_rap_view_list(self):
        
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "project.rap",
            "domain": [('rap_id', '=', self.id)],
            "context": {'default_rap_id':self.id} 
        }

        
   
    

class RapCategory(models.Model):
    _name = 'rap.category'
    _description = 'Rap Category'
    _rec_name = 'product_id'

    rap_id = fields.Many2one('rap.rap', string='RAP',ondelete="cascade")
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet',ondelete="cascade")
    product_id = fields.Many2one('product.product',required=True)
    rab_category_id = fields.Many2one('rab.category', string='Rab Category')
    parent_component_line_ids = fields.One2many('component.component', 'rap_category_id', string='Parent Component Line')
    product_qty = fields.Integer('Product Qty')
    rab_price = fields.Float('RAB Price')
    price_unit = fields.Float('Price')
    subtotal_amount = fields.Float(compute='_compute_subtotal_amount', string='Subtotal')
    rap_state = fields.Selection(related='rap_id.state',store=True)

    
    def action_view_detail_rap(self):
        return {
                'name': 'Component RAP',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'rap.category',
                'target':'new',
                'res_id': self.id,
            }
    
    @api.depends('price_unit','product_qty')
    def _compute_subtotal_amount(self):
        for this in self:
            this.subtotal_amount = this.product_qty * this.price_unit
    
    
    @api.constrains('product_id')
    def _constrains_product_id(self):
        for this in self:
            data = this.env['rab.category'].search([('cost_sheet_id', '=', this.cost_sheet_id.id),('product_id', '=', this.product_id.id)])
            if len(data) > 1:
                raise ValidationError('Cannot create same product in one cost sheet')
            
    
    def action_view_detail(self):
        return {
                'name': 'Component RAB',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'rab.category',
                'target':'new',
                'res_id': self.id,
                }