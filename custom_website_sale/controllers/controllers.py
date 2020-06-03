# -*- coding: utf-8 -*-

import json
import logging
from werkzeug.exceptions import Forbidden
from odoo import http, tools, _
from odoo.exceptions import ValidationError
from odoo.http import request
import odoo.addons.br_website_sale.controllers.main as main_br
import odoo.addons.website_sale.controllers.main as main
from odoo.addons.br_base.tools.fiscal import validate_cnpj, validate_cpf


class CustomBrWebsiteSale(main_br.L10nBrWebsiteSale):

    def checkout_form_validate(self, mode, all_form_values, data):

        ###
        # Website Sale
        ###
        
        # mode: tuple ('new|edit', 'billing|shipping')
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []

        # Required fields from form
        required_fields = [f for f in (all_form_values.get('field_required') or '').split(',') if f]
        # Required fields from mandatory field function
        required_fields += mode[1] == 'shipping' and self._get_mandatory_shipping_fields() or self._get_mandatory_billing_fields()
        # Check if state required
        country = request.env['res.country']
        if data.get('country_id'):
            country = country.browse(int(data.get('country_id')))
            if 'state_code' in country.get_address_fields() and country.state_ids:
                required_fields += ['state_id']

        # error message for empty required fields
        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        Partner = request.env['res.partner']
        if data.get("vat") and hasattr(Partner, "check_vat"):
            if data.get("country_id"):
                data["vat"] = Partner.fix_eu_vat_number(data.get("country_id"), data.get("vat"))
            partner_dummy = Partner.new({
                'vat': data['vat'],
                'country_id': (int(data['country_id'])
                               if data.get('country_id') else False),
            })
            try:
                partner_dummy.check_vat()
            except ValidationError:
                error["vat"] = 'error'

        if [err for err in error.items() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        ###
        # Br Website Sale
        ###
        
        '''
        error, error_message = super(CustomBrWebsiteSale, self).\
            checkout_form_validate(mode, all_form_values, data)
        '''
        
        cnpj_cpf = data.get('cnpj_cpf', '0')
        email = data.get('email', False)
        if cnpj_cpf and len(cnpj_cpf) == 18:
            if not validate_cnpj(cnpj_cpf):
                error["cnpj_cpf"] = u"invalid"
                error_message.append(('CNPJ Inválido!'))
        elif cnpj_cpf and len(cnpj_cpf) == 14:
            if not validate_cpf(cnpj_cpf):
                error["cnpj_cpf"] = u"invalid"
                error_message.append(('CPF Inválido!'))
        partner_id = data.get('partner_id', False)
        '''
        if cnpj_cpf:
            domain = [('cnpj_cpf', '=', cnpj_cpf)]
            if partner_id and mode[0] == 'edit':
                domain.append(('id', '!=', partner_id))
            existe = request.env["res.partner"].sudo().search_count(domain)
            if existe > 0:
                error["cnpj_cpf"] = u"invalid"
                error_message.append(('CPF/CNPJ já cadastrado'))
        if email:
            domain = [('email', '=', email)]
            if partner_id and mode[0] == 'edit':
                domain.append(('id', '!=', partner_id))
            existe = request.env["res.partner"].sudo().search_count(domain)
            if existe > 0:
                error["email"] = u"invalid"
                error_message.append(('E-mail já cadastrado'))
        '''
        if 'city_id' in data and not data['city_id']:
            error["city_id"] = u"missing"
            error_message.append('Selecione uma cidade')
        if 'phone' in data and not data['phone']:
            error["phone"] = u"missing"
            error_message.append('Informe o seu número de telefone')
        return error, error_message
    
    def _checkout_form_save(self, mode, checkout, all_values):
        Partner = request.env['res.partner']
        if mode[0] == 'new':
            existent_partner = request.env['res.partner'].sudo().search([('cnpj_cpf', '=', checkout['cnpj_cpf'])])
            if existent_partner:
                if 'parent_id' in checkout:
                    del checkout['parent_id']
                '''
                if 'type' in checkout:
                    del checkout['type']
                '''
                partner_id = existent_partner.id
                Partner.browse(partner_id).sudo().write(checkout)
            else:
                partner_id = Partner.sudo().create(checkout)
        elif mode[0] == 'edit':
            partner_id = int(all_values.get('partner_id', 0))
            if partner_id:
                # double check
                order = request.website.sale_get_order()
                shippings = Partner.sudo().search(
                    [("id", "child_of",
                      order.partner_id.commercial_partner_id.ids)])
                if partner_id not in shippings.mapped('id') and \
                   partner_id != order.partner_id.id:
                    return Forbidden()

                Partner.browse(partner_id).sudo().write(checkout)
        return partner_id
    