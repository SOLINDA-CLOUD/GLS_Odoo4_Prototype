from odoo import _, api, fields, models

class CostSheetComponent(models.TransientModel):
    _name = 'cost.sheet.component'
    _description = 'Cost Sheet Component'
    
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet')
    # category_line_ids = fields.One2many('rab', 'inverse_field_name', string='Category Line')
    category_id = fields.Many2one('rab.category', string='Category')
    component_ids = fields.Many2many('component.component', string='Component')
    
    
    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id:
            data = self.env['component.component'].search([('cost_sheet_id', '=', self.cost_sheet_id.id),('category_id', '=', self.category_id.id)]).ids
            self.write({
                'component_ids': [(6,0,data)]
            })
        else:
            self.write({
                'component_ids': False
            })
            
    # category_ids = fields.Many2many('rab.category')
    
    
    # oof