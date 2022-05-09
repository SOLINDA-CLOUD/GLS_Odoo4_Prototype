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
                }) for data in self.rab_id.rab_line_ids]

        })
        
        self.write({'rap_id':rap.id})
        
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "rap.rap",
            "res_id": rap.id
        }