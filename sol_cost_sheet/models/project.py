from random import random
from odoo import _, api, fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'


    rab_id = fields.Many2one('cost.sheet',related='sale_order_id.rab_id', string='RAB',store=True)
    rap_id = fields.Many2one('rap.rap', string='RAP')
    # purchase_id = fields.Many2one('purchase.requisition', string='RAP')

    def create_rap(self):
        
        rap = self.env['rap.rap'].create({
                'date_document': fields.Date.today(),
                # 'crm_id': self.rab_id.crm_id.id,
                'project_id': self.id,
                'category_line_ids': [(0,0,{
                    'cost_sheet_id': self.rab_id.id,
                    'rab_category_id': rab.id,
                    'product_id': rab.product_id.id,
                    'rab_price': rab.price,
                    # 'product_qty':
                    'price_unit': rab.price
                
                }) for rab in self.rab_id.category_line_ids]
        })
        
        for category in self.rab_id.category_line_ids:
            for component in category.parent_component_line_ids:
                category_rap = [i for i in rap.category_line_ids if i.rab_category_id.id == category.id]
                component.write({
                    'rap_category_id': category_rap[0] if category_rap else False,
                    'rap_id': rap.id
                })
                for item in component.item_ids:
                    item.write({
                    'rap_category_id': category_rap[0] if category_rap else False,
                    'rap_id': rap.id
                    })
        
        self.write({'rap_id':rap.id})
        # self.rap_id = rap.id
        
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "rap.rap",
            "res_id": rap.id
        }