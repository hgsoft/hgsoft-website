# -*- coding: utf-8 -*-
import werkzeug

from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.website.models.website import slugify as slug

class pos_website_sale(http.Controller):
    @http.route(['/shop/get_order_numbers'], type='json', auth="public", website=True)
    def get_order_numbers(self):
        res = {}
        order = request.website.sale_get_order()
        if order:
            for line in order.website_order_line:
                res[line.product_id.id] = line.product_uom_qty
        return res
