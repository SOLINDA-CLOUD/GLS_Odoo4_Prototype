# -*- coding: utf-8 -*-
# from odoo import http


# class SolCostSheet(http.Controller):
#     @http.route('/sol_cost_sheet/sol_cost_sheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sol_cost_sheet/sol_cost_sheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sol_cost_sheet.listing', {
#             'root': '/sol_cost_sheet/sol_cost_sheet',
#             'objects': http.request.env['sol_cost_sheet.sol_cost_sheet'].search([]),
#         })

#     @http.route('/sol_cost_sheet/sol_cost_sheet/objects/<model("sol_cost_sheet.sol_cost_sheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sol_cost_sheet.object', {
#             'object': obj
#         })
