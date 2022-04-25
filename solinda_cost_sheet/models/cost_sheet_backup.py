from odoo.tools.misc import get_lang
from odoo import _, api, fields, models

class CostSheet(models.Model):
    _name = 'cost.sheet'
    _description = 'Cost Sheet'
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name',tracking=True)
    crm_id = fields.Many2one('crm.lead', string='CRM',tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    date_document = fields.Date('Request Date',tracking=True,default=fields.Date.today)
    user_id = fields.Many2one('res.users', string='Responsible',default=lambda self:self.env.user.id)
    rab_template_id = fields.Many2one('rab.template', string='RAB Template',tracking=True)
    note = fields.Text('Term and condition')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submited'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='Status',tracking=True, default="draft")
    margin_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
    ], string='Margin Type',default='percentage')
    margin_amount_input = fields.Monetary('Margin Amount')
    margin_percent_input = fields.Float('Margin %')
    
    line_ids = fields.One2many('project.rab', 'cost_sheet_id', string='RAB.')  #obsolete
    rab_line_ids = fields.One2many('rab.line', 'cost_sheet_id', string='RAB')
    general_work_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='General Work')
    intake_package_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='Intake Package')
    pretreatment_package_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='Pretreatment Package')
    swro_package_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='SWRO Package')
    brine_injection_package_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='Brine Injection Package')
    product_package_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='Product Package')
    electrical_package_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='Electrical Package')
    civil_work_line_ids = fields.One2many('component.material.rab', 'cost_sheet_id', string='Civil Work')
    

    # purchase_id = fields.Many2one('purchase.requisition', string='Purchase')

    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount',store=True)
    total_margin = fields.Float(compute='_compute_total_amount', string='Total Margin',store=True)
    total_without_margin = fields.Float(compute='_compute_total_amount', string='Price Subtotal',store=True)
    currency_id = fields.Many2one('res.currency', string='currency',default=lambda self:self.env.company.currency_id.id)

    
    # RAB NON PROJECT
    
    
    
    def action_create_requisition(self):
        request = self.env['purchase.requisition'].create({
            'user_id': self.env.uid,
            'ordering_date': fields.Date.today(),
            'origin': self.name,
            'line_ids':[(0,0,{
                'product_id':data.product_id.id,
                'product_description_variants': data.product_id.name,
                'product_qty': data.product_qty,
                'price_unit': data.price_unit
            })for data in self.line_ids if not data.display_type]
        })
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "purchase.requisition",
            "res_id": request.id
        }
    
    @api.depends('margin_amount_input','margin_percent_input')
    def _compute_total_amount(self):
        for this in self:
            total = 0
            total_without_margin = 0
            total_margin = 0
            if this.margin_type == 'percentage':
 
                total = sum(this.line_ids.mapped('price_subtotal'))
                total_without_margin = sum(this.line_ids.mapped('price_subtotal'))
                total_margin = this.margin_percent_input * total_without_margin
            else:
                total = sum(this.line_ids.mapped('price_subtotal')) + this.margin_amount_input
                total_without_margin = sum(this.line_ids.mapped('price_subtotal'))
                total_margin = this.margin_amount_input
                
            this.total_amount = total
            this.total_without_margin = total_without_margin
            this.total_margin = total_margin

    
    @api.onchange('margin_type')
    def _onchange_margin_type(self):
        self.margin_amount_input = 0.0
        self.margin_percent_input = 0.0
    
    @api.onchange('margin_percent_input')
    def _onchange_margin_percent_input(self):
        if self.margin_percent_input:
            self.line_ids.write({'margin_percent':self.margin_percent_input})
        else:
            self.line_ids.write({'margin_percent':self.margin_percent_input})
            
    
    @api.onchange('crm_id')
    def _onchange_crm_id(self):
        if self.crm_id and self.crm_id.partner_id:
            self.partner_id = self.crm_id.partner_id.id
    
    @api.depends('approver_id','approval_id')
    def _compute_is_approver(self):
        for this in self:
            if this.approval_id or this.approver_id:
                if this.approval_id.approval_type == 'user':
                    this.is_approver = this.env.user.id in this.approver_id.user_ids.ids
                else:
                    this.is_approver = this.env.user.id in this.approver_id.group_ids.users.ids
            else:
                this.is_approver = False

    def waiting_approval(self):
        for request in self:
            request.approval_id = request.env['approval.approval'].search([('active', '=', True)],limit=1)
            if bool(request.approver_id):
                approver_id = request.approval_id.approver_line_ids.search([("amount", "<=", request.total_amount),('sequence','>',request.approver_id.sequence)],limit=1)
                if approver_id:
                    request.write({"approver_id": approver_id.id})
                    # request.notify()
                else:
                    request.write({"state_rap": "done","approver_id":False })

            else:
                approver_id = request.approval_id.approver_line_ids.search([("amount", "<=", request.total_amount)],order="sequence ASC",limit=1)
                if approver_id:
                    request.write(
                        {
                            "approver_id": approver_id.id,
                            "state_rap": "waiting",
                        }
                    )
                    # request.notify()
                else:
                    request.write(
                        {
                            "state_rap": "done",
                            "approver_id":False
                        }
                    )
                    

    def action_submit(self):
        self.write({'state':'submit'})
    def action_done(self):
        self.write({'state':'done'})
    def action_to_draft(self):
        self.write({'state':'draft'})
    
    # def create_rap(self):
    #     purchase = self.env['purchase.requisition'].create({
    #         'crm_id': self.crm_id.id,
    #         'origin': self.name,
    #         'date_end' : fields.Datetime.today,
    #         'ordering_date' : fields.Date.today,
    #         'schedule_date' : fields.Date.today,
    #         'line_ids': [(0,0,{
    #             'product_id': template.product_id.id,
    #             'product_qty': template.product_qty,
    #             'product_uom_id': template.uom_id.id,
    #             'product_description_variants' : template.name,
    #             'price_unit': template.price_unit
    #         }) for template in self.line_ids]

    #     })
    #     self.write({'purchase_id':purchase.id})
        
    #     return {
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "purchase.requisition",
    #         "res_id": purchase.id
    #     }

    def action_view_crm(self):
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "crm.lead",
            "res_id": self.crm_id.id
        }
        
    def action_print_rab(self):
        return self.env.ref('solinda_cost_sheet.action_report_cost_sheet').report_action(self)

    @api.model
    def create(self, vals):
        res = super(CostSheet, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("cost.sheet.seq")
        res.crm_id.rab_id = res.id
        return res 
    
   
    @api.onchange('rab_template_id')
    def _onchange_rab_template_id(self):
        if self.line_ids:
            self.write({
                'line_ids': [(5,0,0)]
            })
        else:        
            self.write({
                'line_ids': [(0,0,{
                    'name': template.name,
                    'display_type': template.display_type,
                    'sequence': template.sequence,
                    'product_id': template.product_id.id,
                    'product_qty': template.product_qty,
                    'uom_id': template.uom_id.id,
                    'vol_factor': template.vol_factor,
                    'item_factor': template.item_factor,
                    'lab_factor': template.lab_factor,
                    'start_date': template.start_date,
                    'end_date': template.end_date,
                    'no_pos': template.no_pos,
                    'price_unit': template.price_unit,
                    'margin_percent': template.margin_percent
                }) for template in self.rab_template_id.line_ids]
        }) 

# RAB 

class RabLine(models.Model):
    _name = 'rab.line'
    _description = 'Rab Line'
    
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer('Sequence')
    product_id = fields.Many2one('product.product', string='Product', domain=[('product_group', '!=', False)])
    partner_id = fields.Many2one('res.partner', related='cost_sheet_id.partner_id', string='Partner', readonly=True, store=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    name = fields.Char('Description')
    product_qty = fields.Float('Quantity',default=1.0)
    uom_id = fields.Many2one('uom.uom', string='UoM')
    price_unit = fields.Float(compute='_compute_amount', string='Price',store=True)
    propotional_percent = fields.Float(compute='_compute_amount', string='Propotional %',store=True)
    suggested_proposional_percent = fields.Float(compute='_compute_amount', string='Sug. Commercial Price',store=True)
    commercial_price  = fields.Float('Final Price')
    commercial_price_percentage = fields.Float('Final %')   
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            return

        self.uom_id = self.product_id.uom_po_id or self.product_id.uom_id
        product_lang = self.product_id.with_context(
            lang=get_lang(self.env, self.partner_id.lang).code,
            partner_id=self.partner_id.id,
            company_id=self.env.company.id,
        )
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase
        self.name = name
        
    @api.model
    def create(self, vals):
        res = super(RabLine, self).create(vals)
        data = []
        if res.product_id.product_group == 'general_work':
            if res.product_id.bom_ids:
                data.append({
                'cost_sheet_id': res.cost_sheet_id.id,
                'name': res.product_id.name,
                'display_type': 'line_section',
                'type': 'general_work',
                'rab_line_id': res.id
                })
                for bom in res.product_id.bom_ids[0].rab_component_line_ids:
                    data.append({
                        'type': 'general_work',
                        'cost_sheet_id': res.cost_sheet_id.id,
                        'display_type': False,
                        'product_id': bom.product_id.id,
                        'name': bom.product_id.display_name,
                        'product_qty': bom.product_qty,
                        'uom_id' : bom.product_uom_id.id,
                        'existing_price': bom.product_id.list_price,
                        'rfq_price' : bom.product_id.list_price,
                        'rab_line_id': res.id
                    })            
                res.cost_sheet_id.general_work_line_ids.create(data)
        elif res.product_id.product_group == 'intake_package':
            if res.product_id.bom_ids:
                res.cost_sheet_id.write({
                    'intake_package_line_ids':[(0,0,{
                        'cost_sheet_id': res.cost_sheet_id.id,
                        'name': res.product_id.name,
                        'display_type': 'line_section',
                        'type': 'intake_package',
                        'rab_line_id': res.id
                    })]
                })
                
                res.cost_sheet_id.write({
                    'intake_package_line_ids': [(0,0,{
                    'type': 'intake_package',
                    'cost_sheet_id': res.cost_sheet_id.id,
                    'display_type': False,
                    'product_id': bom.product_id.id,
                    'name': bom.product_id.display_name,
                    'product_qty': bom.product_qty,
                    'uom_id' : bom.product_uom_id.id,
                    'existing_price': bom.product_id.list_price,
                    'rfq_price' : bom.product_id.list_price,
                    'rab_line_id': res.id
                }) for bom in res.product_id.bom_ids[0].rab_component_line_ids]
                })
                
        elif res.product_id.product_group == 'pretreatment_package':
            res
        elif res.product_id.product_group == 'swro_package':
            res
        elif res.product_id.product_group == 'brine_injection_package':
            res
        elif res.product_id.product_group == 'product_package':
            res
        elif res.product_id.product_group == 'electrical_package':
            res
        elif res.product_id.product_group == 'civil_work':
            res
        elif res.product_id.product_group == 'ga_project':
            res
        elif res.product_id.product_group == 'waranty':
            res
        return res
        
        

    
    
    @api.depends(
        'cost_sheet_id.general_work_line_ids',
        'cost_sheet_id.general_work_line_ids.rfq_price',
        'cost_sheet_id.general_work_line_ids.product_qty',
        'cost_sheet_id.intake_package_line_ids',
        'cost_sheet_id.intake_package_line_ids.rfq_price',
        'cost_sheet_id.intake_package_line_ids.product_qty',
        'cost_sheet_id.pretreatment_package_line_ids',
        'cost_sheet_id.pretreatment_package_line_ids.rfq_price',
        'cost_sheet_id.pretreatment_package_line_ids.product_qty',
        'cost_sheet_id.swro_package_line_ids',
        'cost_sheet_id.swro_package_line_ids.rfq_price',
        'cost_sheet_id.swro_package_line_ids.product_qty',
        'cost_sheet_id.brine_injection_package_line_ids',
        'cost_sheet_id.brine_injection_package_line_ids.rfq_price',
        'cost_sheet_id.brine_injection_package_line_ids.product_qty',
        'cost_sheet_id.product_package_line_ids',
        'cost_sheet_id.product_package_line_ids.rfq_price',
        'cost_sheet_id.product_package_line_ids.product_qty',
        'cost_sheet_id.electrical_package_line_ids',
        'cost_sheet_id.electrical_package_line_ids.rfq_price',
        'cost_sheet_id.electrical_package_line_ids.product_qty',
        'cost_sheet_id.civil_work_line_ids',
        'cost_sheet_id.civil_work_line_ids.rfq_price',
        'cost_sheet_id.civil_work_line_ids.product_qty'
        )
    def _compute_amount(self):
        for this in self:
            amount = 0
            print(">>>>>>>>>>",self._origin)
            print(">>>>>>>>>>",this)
            
            # if not this.display_type and this.product_id:
            #     data_product = this.env['component.material.rab'].search([('type', '=', this.product_id.product_group),('cost_sheet_id.id', '=', this.cost_sheet_id._origin.id)])
            #     this.price_unit = sum(data_product.mapped('total_price'))
            #     this.propotional_percent = this.price_unit / sum(this.cost_sheet_id.mapped('rab_line_ids.price_unit'))
            #     print('><><><><><><><><><><>',sum(this.cost_sheet_id.mapped('rab_line_ids.price_unit')))
            #     print('><><><><><><><><><><>',this.price_unit)
            #     print('><><><><><><><><><><>',this.price_unit / sum(this.cost_sheet_id.mapped('rab_line_ids.price_unit')))
            #     this.suggested_proposional_percent = amount
            # else:
            this.price_unit = amount
            this.propotional_percent = amount
            this.suggested_proposional_percent = amount
                
    
    
class ComponentMaterialRAB(models.Model):
    _name = 'component.material.rab'
    _description = 'Component Material RAB'
    
    
    type = fields.Selection([
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
    ], string='type')
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer('Sequence')
    product_id = fields.Many2one('product.product', string='Product')
    partner_id = fields.Many2one('res.partner', related='cost_sheet_id.partner_id', string='Partner', readonly=True, store=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    name = fields.Char('Description')
    note = fields.Char('Remarks')
    product_qty = fields.Float('Quantity',default=1.0)
    uom_id = fields.Many2one('uom.uom', string='UoM')
    existing_price = fields.Float('Existing Price',related="product_id.list_price",store=True)
    rfq_price = fields.Float('RFQ Price')
    total_price = fields.Float(compute='_compute_total_price', string='Total Price',store=True)
    rab_line_id = fields.Many2one('rab.line', string='RAB Line')
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.product_id:
            return

        self.uom_id = self.product_id.uom_po_id or self.product_id.uom_id
        product_lang = self.product_id.with_context(
            lang=get_lang(self.env, self.partner_id.lang).code,
            partner_id=self.partner_id.id,
            company_id=self.env.company.id,
        )
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase
        self.name = name
        
        self.rfq_price = self.product_id.list_price


    @api.depends('product_qty','rfq_price')
    def _compute_total_price(self):
        for this in self:
            total = 0.0
            total = this.product_qty * this.rfq_price
            this.total_price = total




class ProjectRab(models.Model):
    _name = 'project.rab'
    _description = 'Project RAB'

    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet')
    rab_template_id = fields.Many2one('rab.template', string='RAB Template')
    # project_id = fields.Many2one('project.project', string='Project')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer('Sequence')

    product_id = fields.Many2one('product.product', string='Product')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)

    name = fields.Char('Description')
    
    product_qty = fields.Float('Quantity',default=1.0)
    uom_id = fields.Many2one('uom.uom', string='UoM')
    vol_factor = fields.Float('Volume Factor')
    item_factor = fields.Float('Item Factor')
    lab_factor = fields.Float('Lab Factor')
    price_unit = fields.Float('Price')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('Finish Date')
    no_pos = fields.Char('No')
    margin = fields.Float('Margin',compute='_compute_price')
    margin_percent = fields.Float(string='Margin Percent',compute='_compute_price')
    price_subtotal = fields.Float(compute='_compute_price', string='Subtotal')
    
    price_final = fields.Float('Price Final')    
    
    def create_requisition(self):
        request = self.env['purchase.requisition'].create({
            'user_id': self.env.uid,
            'ordering_date': fields.Date.today(),
            'origin': self.cost_sheet_id.name,
            'line_ids':[(0,0,{
                'product_id':self.product_id.id,
                'product_qty': self.product_qty,
                'price_unit': self.price_unit
            })]
        })
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "purchase.requisition",
            "res_id": request.id
        }


    
    @api.depends('price_unit','cost_sheet_id.margin_percent_input','cost_sheet_id.margin_amount_input')
    def _compute_price(self):
        for this in self:
            margin = 0.0
            margin_percent = 0.0
            subtotal = 0.0
            if this.cost_sheet_id.margin_type == 'percentage':
                margin_percent = this.cost_sheet_id.margin_percent_input
                margin = this.price_unit * margin_percent
                subtotal = this.price_unit * this.product_qty + margin
            else:
                margin_percent = 0.0
                margin = 0.0
                subtotal = this.price_unit * this.product_qty 
               
                
            this.margin = margin
            this.margin_percent = margin_percent
            this.price_subtotal = subtotal
            


class RabTemplate(models.Model):
    _name = 'rab.template'
    _description = 'RAB Template'

    name = fields.Char('Name of Template')
    line_ids = fields.One2many('project.rab', 'rab_template_id', string='Rab Line')

    
