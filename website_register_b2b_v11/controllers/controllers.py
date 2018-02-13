# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm

class WebsiteRegisterB2bV11(http.Controller):
     @http.route('/page/register', type='http', auth='public', website=True)
     def index(self, **kw):
        #return "Hello, world"
        #return http.request.render('website.register', {})
    
        countries = http.request.env['res.country']
        
        states = http.request.env['res.country.state']

        values = {
                'countries': countries.search([]),
                'states': states.search([]),
         }
        return http.request.render('website.register', values)
    
        """
        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(int(values['country_id']))
        country = country and country.exists() or def_country_id
        render_values = {
                'partner_id': partner_id,
                'mode': mode,
                'checkout': values,
                'country': country,
                'countries': country.get_website_sale_countries(mode=mode[1]),
                "states": country.get_website_sale_states(mode=mode[1]),
                'error': errors,
                'callback': kw.get('callback'),
        }
        #return request.render("website_sale.address", render_values)
        return http.request.render('website.register', render_values)
        """
        
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
    
