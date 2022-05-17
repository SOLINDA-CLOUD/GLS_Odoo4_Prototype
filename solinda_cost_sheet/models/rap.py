from odoo import _, api, fields, models

class CsRAP(models.Model):
    _name = 'rap.rap'
    _description = 'RAP'
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name',tracking=True)
    crm_id = fields.Many2one('crm.lead', string='CRM',tracking=True)
    project_id = fields.Many2one('project.project', string='Project')
    date_document = fields.Date('Request Date',tracking=True,default=fields.Date.today)
    user_id = fields.Many2one('res.users', string='Responsible',default=lambda self:self.env.user.id)
    # rab_template_id = fields.Many2one('rab.template', string='RAB Template',tracking=True)
    line_ids = fields.One2many('project.rap', 'rap_id', string='RAP')  
    note = fields.Text('Term and condition')
    approval_id = fields.Many2one('approval.approval', string='Approval')
    approver_id = fields.Many2one('approver.line', string='Approver')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submited'),
        ('waiting', 'Waiting Approval'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='Status',tracking=True, default="draft")

    # purchase_id = fields.Many2one('purchase.requisition', string='Purchase')

    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount',store=True)
    total_margin = fields.Float(compute='_compute_total_amount', string='Margin',store=True)
    total_without_margin = fields.Float(compute='_compute_total_amount', string='Price Subtotal',store=True)
    currency_id = fields.Many2one('res.currency', string='currency',default=lambda self:self.env.company.currency_id.id)
    is_approver = fields.Boolean(compute='_compute_is_approver', string='Is Approver')
    
    
    general_work_line_ids = fields.One2many('general.work', 'rap_id', string='General Work',copy=True)
    intake_package_line_ids = fields.One2many('intake.package', 'rap_id', string='Intake Package',copy=True)
    pretreatment_package_line_ids = fields.One2many('pretreatment.package', 'rap_id', string='Pretreatment Package',copy=True)
    swro_package_line_ids = fields.One2many('swro.package', 'rap_id', string='SWRO Package',copy=True)
    brine_injection_package_line_ids = fields.One2many('brine.injection.package', 'rap_id', string='Brine Injection Package',copy=True)
    product_package_line_ids = fields.One2many('product.package', 'rap_id', string='Product Package',copy=True)
    electrical_package_line_ids = fields.One2many('electrical.package', 'rap_id', string='Electrical Package',copy=True)
    civil_work_line_ids = fields.One2many('civil.work', 'rap_id', string='Civil Work',copy=True)
    ga_project_line_ids = fields.One2many('ga.project', 'rap_id',copy=True)
    waranty_line_ids = fields.One2many('waranty.waranty', 'rap_id',copy=True)
    ion_exchange_line_ids = fields.One2many('ion.exchange.package', 'rap_id',copy=True)
    media_filter_line_ids = fields.One2many('media.filter.package', 'rap_id',copy=True)
    carbon_filter_line_ids = fields.One2many('carbon.filter.package', 'rap_id',copy=True)
    softener_line_ids = fields.One2many('softener.package', 'rap_id',copy=True)
    electrode_ionization_line_ids = fields.One2many('electrodeionization.package', 'rap_id',copy=True)
    product_tank_line_ids = fields.One2many('product.tank.package', 'rap_id',copy=True)
    demin_tank_line_ids = fields.One2many('demin.tank.package', 'rap_id',copy=True)
    brine_line_ids = fields.One2many('brine.package', 'rap_id',copy=True)
    sludge_dewatering_line_ids = fields.One2many('sludge.dewatering.package', 'rap_id',copy=True)
    interconnecting_line_ids = fields.One2many('interconnecting.package', 'rap_id',copy=True)
    major_pumps_line_ids = fields.One2many('major.pumps.package', 'rap_id',copy=True)
    uv_line_ids = fields.One2many('uv.package', 'rap_id',copy=True)
    chemical_line_ids = fields.One2many('chemical.package', 'rap_id',copy=True)
    cip_line_ids = fields.One2many('cip.package', 'rap_id',copy=True)
    installation_line_ids = fields.One2many('installation.package', 'rap_id',copy=True)
    test_commissioning_line_ids = fields.One2many('test.commissioning.package', 'rap_id',copy=True)
    cation_exchange_line_ids = fields.One2many('cation.exchange.package', 'rap_id',copy=True)
    anion_exchange_line_ids = fields.One2many('anion.exchange.package', 'rap_id',copy=True)
    civil_construction_line_ids = fields.One2many('civil.construction.package', 'rap_id',copy=True)
    fbr_line_ids = fields.One2many('fbr.package', 'rap_id',copy=True)
    other1_line_ids = fields.One2many('other1.package', 'rap_id',copy=True)
    other2_line_ids = fields.One2many('other2.package', 'rap_id',copy=True)
    other3_line_ids = fields.One2many('other3.package', 'rap_id',copy=True)
    other4_line_ids = fields.One2many('other4.package', 'rap_id',copy=True)
    other5_line_ids = fields.One2many('other5.package', 'rap_id',copy=True)

    
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

        
    def action_submit(self):
        
        self.write({'state':'submit'})
        self.waiting_approval()

    def action_done(self):
        self.write({'state':'done'})
    def action_to_draft(self):
        self.write({'state':'draft','approval_id':False,'approver_id':False})
    
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

    # def action_view_crm(self):
    #     return {
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "crm.lead",
    #         "res_id": self.crm_id.id
    #     }

    @api.model
    def create(self, vals):
        res = super(CsRAP, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("rap.rap")
        res.crm_id.rab_id = res.id
        return res 
    
    @api.depends('line_ids.price_subtotal','line_ids.margin','line_ids.price_unit')
    def _compute_total_amount(self):
        for this in self:
            this.total_amount = sum(this.line_ids.mapped('price_subtotal'))
            this.total_without_margin = sum(this.line_ids.mapped('price_unit'))
            this.total_margin = sum(this.line_ids.mapped('margin'))

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

class ProjectRab(models.Model):
    _name = 'project.rap'
    _description = 'Project RAP'

    rap_id = fields.Many2one('rap.rap', string='RAP')
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
    rab_price = fields.Float('RAB Price')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('Finish Date')
    no_pos = fields.Char('No')
    margin = fields.Float('Margin',compute='_compute_price')
    margin_percent = fields.Float( string='Margin Percent')
    price_subtotal = fields.Float(compute='_compute_price', string='Subtotal')

    
    @api.depends('margin_percent','price_unit')
    def _compute_price(self):
        for this in self:
            amount = 0
            amount = this.price_unit * this.margin_percent
            this.margin = amount
            this.price_subtotal = this.price_unit + amount
            
    def create_requisition(self):
        request = self.env['purchase.requisition'].create({
            'user_id': self.env.uid,
            'ordering_date': fields.Date.today(),
            'origin': self.rap_id.name,
            'line_ids':[(0,0,{
                'product_id':self.product_id.id,
                'product_qty': self.product_qty,
                'price_unit': self.price_unit
            })for data in self]
        })
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "purchase.requisition",
            "res_id": request.id
        }
