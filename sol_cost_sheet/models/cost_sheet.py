from pkg_resources import require
from odoo import _, api, fields, models

class CostSheet(models.Model):
    _name = 'cost.sheet'
    _description = 'Cost Sheet'
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name',tracking=True)
    crm_id = fields.Many2one('crm.lead', string='CRM',tracking=True,copy=True)
    partner_id = fields.Many2one('res.partner', string='Customer',copy=True)
    date_document = fields.Date('Request Date',tracking=True,default=fields.Date.today)
    user_id = fields.Many2one('res.users', string='Responsible',default=lambda self:self.env.user.id)
    rab_template_id = fields.Many2one('rab.template', string='RAB Template',tracking=True,copy=True)
    note = fields.Text('Term and condition',copy=True)
    tax_ids = fields.Many2many('account.tax', string='Taxs',copy=True)
    tax_id = fields.Many2one('account.tax', string='Tax',copy=True)
    rev = fields.Integer('Revision')
    revisied = fields.Boolean('Revisied')
    cost_sheet_revision_id = fields.Many2one('cost.sheet', string='Cost Sheet Revision')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submited'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='Status',tracking=True, default="draft")
    
    component_rab_line_ids = fields.One2many('costsheet.component', 'cost_sheet_id', string='Component RAB Line')


class CostSheetComponent(models.Model):
    _name = 'costsheet.component'
    _description = 'Cost Sheet Component'
    _rec_name = "product_id"
    
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet',ondelete="cascade")
    is_header = fields.Boolean('Header')
    is_parent = fields.Boolean('Parent')
    is_child = fields.Boolean('Child')
    
    product_id = fields.Many2one('product.product', string='Product',required=True)
    quantity = fields.Integer('Quantity')
    uom_id = fields.Many2one('uom.uom', string='UoM')
    existing_price = fields.Float('Existing Price')
    rfq_price = fields.Float('RFQ Price')
    remarks = fields.Text('Remarks')
    component_id = fields.Many2one('costsheet.component', string='Component Child', ondelete="cascade")
    component_header_id = fields.Many2one('costsheet.component', string='Component Header', ondelete="cascade")
    component_parent_id = fields.Many2one('costsheet.component', string='Component Parent', ondelete="cascade")
    component_rab_header_line_ids = fields.One2many('costsheet.component', 'component_header_id', string='Component Header RAB Line')
    component_rab_parent_line_ids = fields.One2many('costsheet.component', 'component_parent_id', string='Component Parent RAB Line')
    component_rab_line_ids = fields.One2many('costsheet.component', 'component_id', string='Component RAB Line')
    total_price = fields.Float(compute='_compute_total_price', string='Total Price')
    
    # component_line_ids = fields.One2many('costsheet.component.line', 'component_id', string='Component Line')
    @api.onchange('component_parent_id')
    def _onchange_component_parent_id(self):
        if self.component_parent_id:
            self.cost_sheet_id = self.component_parent_id.cost_sheet_id
    
    @api.depends('quantity','rfq_price')
    def _compute_total_price(self):
        for this in self:
            total = 0.0
            total = this.quantity * this.rfq_price
            this.total_price = total
    

class ComponentParent(models.Model):
    _name = 'component.parent'
    _description = 'Component Parent'

    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet',ondelete="cascade")
    is_header = fields.Boolean('Header')
    is_parent = fields.Boolean('Parent')
    is_child = fields.Boolean('Child')
    
    product_id = fields.Many2one('product.product', string='Product',required=True)
    quantity = fields.Integer('Quantity')
    uom_id = fields.Many2one('uom.uom', string='UoM')
    existing_price = fields.Float('Existing Price')
    rfq_price = fields.Float('RFQ Price')
    remarks = fields.Text('Remarks')
    component_id = fields.Many2one('costsheet.component', string='Component Child', ondelete="cascade")
    component_header_id = fields.Many2one('costsheet.component', string='Component Header', ondelete="cascade")
    component_parent_id = fields.Many2one('costsheet.component', string='Component Parent', ondelete="cascade")
    component_rab_header_line_ids = fields.One2many('costsheet.component', 'component_header_id', string='Component Header RAB Line')
    component_rab_parent_line_ids = fields.One2many('costsheet.component', 'component_parent_id', string='Component Parent RAB Line')
    component_rab_line_ids = fields.One2many('costsheet.component', 'component_id', string='Component RAB Line')
    total_price = fields.Float(compute='_compute_total_price', string='Total Price')
    
    # component_line_ids = fields.One2many('costsheet.component.line', 'component_id', string='Component Line')
    @api.onchange('component_parent_id')
    def _onchange_component_parent_id(self):
        if self.component_parent_id:
            self.cost_sheet_id = self.component_parent_id.cost_sheet_id
    
    @api.depends('quantity','rfq_price')
    def _compute_total_price(self):
        for this in self:
            total = 0.0
            total = this.quantity * this.rfq_price
            this.total_price = total
            
class ComponentParent(models.Model):
    _name = 'component.parent'
    _description = 'Component Parent'
    
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet',ondelete="cascade")
    is_header = fields.Boolean('Header')
    is_parent = fields.Boolean('Parent')
    is_child = fields.Boolean('Child')
    
    product_id = fields.Many2one('product.product', string='Product',required=True)
    quantity = fields.Integer('Quantity')
    uom_id = fields.Many2one('uom.uom', string='UoM')
    existing_price = fields.Float('Existing Price')
    rfq_price = fields.Float('RFQ Price')
    remarks = fields.Text('Remarks')
    component_id = fields.Many2one('costsheet.component', string='Component Child', ondelete="cascade")
    component_header_id = fields.Many2one('costsheet.component', string='Component Header', ondelete="cascade")
    component_parent_id = fields.Many2one('costsheet.component', string='Component Parent', ondelete="cascade")
    component_rab_header_line_ids = fields.One2many('costsheet.component', 'component_header_id', string='Component Header RAB Line')
    component_rab_parent_line_ids = fields.One2many('costsheet.component', 'component_parent_id', string='Component Parent RAB Line')
    component_rab_line_ids = fields.One2many('costsheet.component', 'component_id', string='Component RAB Line')
    total_price = fields.Float(compute='_compute_total_price', string='Total Price')
    
    # component_line_ids = fields.One2many('costsheet.component.line', 'component_id', string='Component Line')
    @api.onchange('component_parent_id')
    def _onchange_component_parent_id(self):
        if self.component_parent_id:
            self.cost_sheet_id = self.component_parent_id.cost_sheet_id
    
    @api.depends('quantity','rfq_price')
    def _compute_total_price(self):
        for this in self:
            total = 0.0
            total = this.quantity * this.rfq_price
            this.total_price = total
            

    