# -*- coding: utf-8 -*-
# from odoo import http


# class SolindaSaleOrder(http.Controller):
#     @http.route('/solinda_sale_order/solinda_sale_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/solinda_sale_order/solinda_sale_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('solinda_sale_order.listing', {
#             'root': '/solinda_sale_order/solinda_sale_order',
#             'objects': http.request.env['solinda_sale_order.solinda_sale_order'].search([]),
#         })

#     @http.route('/solinda_sale_order/solinda_sale_order/objects/<model("solinda_sale_order.solinda_sale_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('solinda_sale_order.object', {
#             'object': obj
#         })
