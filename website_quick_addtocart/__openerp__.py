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
{
    'name': 'Website Quick AddToCart',
    'version': '8.0.1.0',
    'category': 'Website',
    'author': 'Geminate Consultancy Services',
    'sequence': 15,
    'description': """

    This module provides a quicker way to add product to shopping cart by excluding extra layer of 'Continue Shopping' shopping cart page.

    You can go back by simply click on breadcrumb of product page.

    NOTE : This feature will not work when website_sale_options app is installed.

    """,
    'website': 'http://www.geminatecs.com/',
    'depends': ['website_sale'],
    'data': [
             "views/website_view.xml", 
             ],
    'demo': [],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
