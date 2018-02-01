# -*- coding: utf-8 -*-
from odoo import http

class WebsiteRegisterB2bV11(http.Controller):
     @http.route('/page/register', type='http', auth='public', website=True)
     def index(self, **kw):
        #return "Hello, world"
        return http.request.render('website.register', {})

#     @http.route('/website_register_b2b_v11/website_register_b2b_v11/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_register_b2b_v11.listing', {
#             'root': '/website_register_b2b_v11/website_register_b2b_v11',
#             'objects': http.request.env['website_register_b2b_v11.website_register_b2b_v11'].search([]),
#         })

#     @http.route('/website_register_b2b_v11/website_register_b2b_v11/objects/<model("website_register_b2b_v11.website_register_b2b_v11"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_register_b2b_v11.object', {
#             'object': obj
#         })