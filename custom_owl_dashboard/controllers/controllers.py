# -*- coding: utf-8 -*-
# from odoo import http


# class CustomOwlDashboard(http.Controller):
#     @http.route('/custom_owl_dashboard/custom_owl_dashboard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_owl_dashboard/custom_owl_dashboard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_owl_dashboard.listing', {
#             'root': '/custom_owl_dashboard/custom_owl_dashboard',
#             'objects': http.request.env['custom_owl_dashboard.custom_owl_dashboard'].search([]),
#         })

#     @http.route('/custom_owl_dashboard/custom_owl_dashboard/objects/<model("custom_owl_dashboard.custom_owl_dashboard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_owl_dashboard.object', {
#             'object': obj
#         })

