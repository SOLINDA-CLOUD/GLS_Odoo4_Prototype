from odoo import _, api, fields, models

class ApprovalApproval(models.Model):
    _name = 'approval.approval'
    _description = 'Approval Approval'
    

    name = fields.Char('name',required=True)
    approver_line_ids = fields.One2many('approver.line', 'approval_id', string='Approver Line')
    active = fields.Boolean('Active',default=True)
    approval_type = fields.Selection([
        ('user', 'By User'),
        ('group', 'By Group'),
    ], string='Approval Type',default='user')


class ApproverLine(models.Model):
    _name = 'approver.line'
    _description = 'Approver Line'
    
    approval_id = fields.Many2one('approval.approval', string='Approval')
    sequence = fields.Integer('sequence')
    name = fields.Char('Name')
    amount = fields.Float('Minimum Approval Amount')
    user_ids = fields.Many2many('res.users', string='User')
    group_ids = fields.Many2many('res.groups', string='Group')
