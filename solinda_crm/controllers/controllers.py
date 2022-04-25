# -*- coding: utf-8 -*-
# from odoo import http


# class SolindaCrm(http.Controller):
#     @http.route('/solinda_crm/solinda_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/solinda_crm/solinda_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('solinda_crm.listing', {
#             'root': '/solinda_crm/solinda_crm',
#             'objects': http.request.env['solinda_crm.solinda_crm'].search([]),
#         })

#     @http.route('/solinda_crm/solinda_crm/objects/<model("solinda_crm.solinda_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('solinda_crm.object', {
#             'object': obj
#         })
