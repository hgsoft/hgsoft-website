# -*- coding: utf-8 -*-
{
    'name': "website_register_b2b",

    'summary': """
        Registration form for site purchases  """,

    'description': """
        Registration form for site purchases
    """,

    'author': "Alexsandro Haag <alex@hgsoft.com.br>, HGSOFT",
    'website': "http://www.hgsoft.com.br",
    'category': 'Website',
    'version': '10.0.1',
    'depends': ['base','website_sale'],
    'data': [
        'views/register.xml',
    ],
    'installable': True,
    'auto_install': False,
}
