# -*- coding: utf-8 -*-
# from odoo import http


# class Manageleire(http.Controller):
#     @http.route('/manageleire/manageleire', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manageleire/manageleire/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manageleire.listing', {
#             'root': '/manageleire/manageleire',
#             'objects': http.request.env['manageleire.manageleire'].search([]),
#         })

#     @http.route('/manageleire/manageleire/objects/<model("manageleire.manageleire"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manageleire.object', {
#             'object': obj
#         })
