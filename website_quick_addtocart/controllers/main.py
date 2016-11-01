# -*- coding: utf-8 -*-
###############################################################################
#
#   website_quick_addtocart for Odoo
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request

class website_sale(http.Controller):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
        product_tmpl_id = request.registry['product.product'].read(cr, SUPERUSER_ID, int(product_id), ['product_tmpl_id'], context=context).get('product_tmpl_id')
        product_name = product_tmpl_id and product_tmpl_id[1].replace(" ", "-").replace(".", "-") + "-" + str(product_tmpl_id[0]) + "#?added=true"
        return request.redirect("/shop/product/" + product_name.lower())
# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
