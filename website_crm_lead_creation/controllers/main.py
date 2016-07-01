'''
Created on 09/08/2015

@author: danimar
'''
from openerp.addons.website_crm.controllers.main import contactus
from openerp.addons.web import http
from openerp.http import request

class ContactUs(contactus):
    
    @http.route()
    def contactus(self, **kwargs):
        try:
            retorno = super(ContactUs, self).contactus(**kwargs)
            
            return retorno
        except Exception as e:
            request._cr.rollback()
            values = {}
            for field_name, field_value in kwargs.items():
                values[field_name] = field_value
            error = set([])
            erros = e.message if e.message else e.value
            values = dict(values, error=error, erros=erros, kwargs=kwargs.items())
            return request.website.render(kwargs.get("view_from", "website.contactus"), values)