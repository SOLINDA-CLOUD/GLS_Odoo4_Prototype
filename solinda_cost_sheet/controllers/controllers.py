# -*- coding: utf-8 -*-
# from odoo import http


# class SolindaCostSheet(http.Controller):
#     @http.route('/solinda_cost_sheet/solinda_cost_sheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/solinda_cost_sheet/solinda_cost_sheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('solinda_cost_sheet.listing', {
#             'root': '/solinda_cost_sheet/solinda_cost_sheet',
#             'objects': http.request.env['solinda_cost_sheet.solinda_cost_sheet'].search([]),
#         })

#     @http.route('/solinda_cost_sheet/solinda_cost_sheet/objects/<model("solinda_cost_sheet.solinda_cost_sheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('solinda_cost_sheet.object', {
#             'object': obj
#         })
