# -*- coding: utf-8 -*-
from odoo import http

class Register(http.Controller):
    @http.route('/page/register', type='http', auth='public', website=True)
    def index(self, **kw):
        return "Hello, world"