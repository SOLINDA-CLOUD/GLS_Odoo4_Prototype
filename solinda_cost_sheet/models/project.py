from odoo import _, api, fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'


    rab_id = fields.Many2one('cost.sheet',related='sale_order_id.rab_id', string='RAB',store=True)
    rap_id = fields.Many2one('rap.rap', string='RAP Plan')
    purchase_id = fields.Many2one('purchase.requisition', string='RAP')

    def create_rap(self):
        # purchase = self.env['purchase.requisition'].create({
        #     'crm_id': self.sale_order_id.rab_id.crm_id.id,
        #     'origin': self.name,
        #     'date_end' : fields.Datetime.now(),
        #     'ordering_date' : fields.Date.today(),
        #     'schedule_date' : fields.Date.today(),
        #     'line_ids': [(0,0,{
        #         'product_id': template.product_id.id,
        #         'product_qty': template.product_qty,
        #         'product_uom_id': template.uom_id.id,
        #         'product_description_variants' : template.name,
        #         'price_unit': template.price_unit
        #     }) for template in self.rab_id.line_ids if template.product_id]
        # })
        rap = self.env['rap.rap'].create({
                'date_document': fields.Date.today(),
                'line_ids' : [(0,0,{
                  'name': data.name,
                    'display_type': data.display_type,
                    'sequence': data.sequence,
                    'product_id': data.product_id.id,
                    'product_qty': data.product_qty,
                    'uom_id': data.uom_id.id,
                    'rab_price': data.price_unit,
                    'price_unit': data.price_unit,
                }) for data in self.rab_id.rab_line_ids],

        })
        self.rab_id.general_work_line_ids.write({'rap_id':rap.id})
        self.rab_id.intake_package_line_ids.write({'rap_id':rap.id})
        self.rab_id.pretreatment_package_line_ids.write({'rap_id':rap.id})
        self.rab_id.swro_package_line_ids.write({'rap_id':rap.id})
        self.rab_id.brine_injection_package_line_ids.write({'rap_id':rap.id})
        self.rab_id.product_package_line_ids.write({'rap_id':rap.id})
        self.rab_id.electrical_package_line_ids.write({'rap_id':rap.id})
        self.rab_id.civil_work_line_ids.write({'rap_id':rap.id})
        self.rab_id.ga_project_line_ids.write({'rap_id':rap.id})
        self.rab_id.waranty_line_ids.write({'rap_id':rap.id})
        self.rab_id.ion_exchange_line_ids.write({'rap_id':rap.id})
        self.rab_id.media_filter_line_ids.write({'rap_id':rap.id})
        self.rab_id.carbon_filter_line_ids.write({'rap_id':rap.id})
        self.rab_id.softener_line_ids.write({'rap_id':rap.id})
        self.rab_id.electrode_ionization_line_ids.write({'rap_id':rap.id})
        self.rab_id.product_tank_line_ids.write({'rap_id':rap.id})
        self.rab_id.demin_tank_line_ids.write({'rap_id':rap.id})
        self.rab_id.brine_line_ids.write({'rap_id':rap.id})
        self.rab_id.sludge_dewatering_line_ids.write({'rap_id':rap.id})
        self.rab_id.interconnecting_line_ids.write({'rap_id':rap.id})
        self.rab_id.major_pumps_line_ids.write({'rap_id':rap.id})
        self.rab_id.uv_line_ids.write({'rap_id':rap.id})
        self.rab_id.chemical_line_ids.write({'rap_id':rap.id})
        self.rab_id.cip_line_ids.write({'rap_id':rap.id})
        self.rab_id.installation_line_ids.write({'rap_id':rap.id})
        self.rab_id.test_commissioning_line_ids.write({'rap_id':rap.id})
        self.rab_id.cation_exchange_line_ids.write({'rap_id':rap.id})
        self.rab_id.anion_exchange_line_ids.write({'rap_id':rap.id})
        self.rab_id.civil_construction_line_ids.write({'rap_id':rap.id})
        self.rab_id.fbr_line_ids.write({'rap_id':rap.id})
        self.rab_id.other1_line_ids.write({'rap_id':rap.id})
        self.rab_id.other2_line_ids.write({'rap_id':rap.id})
        self.rab_id.other3_line_ids.write({'rap_id':rap.id})
        self.rab_id.other4_line_ids.write({'rap_id':rap.id})
        self.rab_id.other5_line_ids.write({'rap_id':rap.id})

        
        self.write({'rap_id':rap.id})
        
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "rap.rap",
            "res_id": rap.id
        }