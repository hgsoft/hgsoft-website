# -*- coding: utf-8 -*-
{
    'name': "website_anonymous_hide_prices",

    'summary': """
        Hide prices, quantity select and "add to cart" button if user is not authenticated""",

    'description': """
        Adds some Qweb views to replace sections on page which will be hidden if user ist not authenticated
    """,

    'author': "Michael Hucke, extended by HGSOFT",
    'website': "http://www.hgsoft.com.br",
    'contributors': ['Alexsandro Haag <alex@hgsoft.com.br>'],
    'category': 'website',
    'version': '10.0.2',
    #'depends': ['base','website_sale','website_register_b2b_v11'],
    'depends': ['base','website_sale'],
    'data': [
        'templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
