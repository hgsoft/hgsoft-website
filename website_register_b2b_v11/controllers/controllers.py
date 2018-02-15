# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm

class WebsiteRegisterB2bV11(http.Controller):
     @http.route('/page/register', type='http', auth='public', website=True)
     def index(self, **kw):
        #return "Hello, world"
        #return http.request.render('website.register', {})
    
        #countries = http.request.env['res.country']
        #states = http.request.env['res.country.state']

        countries = request.env['res.country'].sudo().search([])
        #states = request.env['res.country.state'].sudo().search([])

        values = {
                'countries': countries.search([]),
                #'states': states.search([]),
         }
        return http.request.render('website.register', values)

class WebsiteForm(WebsiteForm):
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if model_name == 'crm.lead' and not request.params.get('state_id'):
            geoip_country_code = request.session.get('geoip', {}).get('country_code')
            geoip_state_code = request.session.get('geoip', {}).get('region')
            if geoip_country_code and geoip_state_code:
                State = request.env['res.country.state']
                request.params['state_id'] = State.search([('code', '=', geoip_state_code), ('country_id.code', '=', geoip_country_code)]).id

        return super(WebsiteForm, self).website_form(model_name, **kwargs)
    
