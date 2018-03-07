# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import re

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.multi
    def handle_partner_assignation(self,  action='create', partner_id=False):
        
        print ("##### handle_partner_assignation [START] #####")
        
        """ Handle partner assignation during a lead conversion.
            if action is 'create', create new partner with contact and assign lead to new partner_id.
            otherwise assign lead to the specified partner_id

            :param list ids: leads/opportunities ids to process
            :param string action: what has to be done regarding partners (create it, assign an existing one, or nothing)
            :param int partner_id: partner to assign if any
            :return dict: dictionary organized as followed: {lead_id: partner_assigned_id}
        """
        partner_ids = {}
        for lead in self:
            if lead.partner_id:
                partner_ids[lead.id] = lead.partner_id.id
                continue
            if action == 'create' or action == 'create_both':
                partner = lead._create_lead_partner()
                partner_id = partner.id
                partner.team_id = lead.team_id
            if partner_id:
                lead.partner_id = partner_id
            partner_ids[lead.id] = partner_id
        
        print ("##### handle_partner_assignation [END] #####")
        
        return partner_ids
        
    @api.multi
    def _lead_create_contact(self, name, is_company, parent_id=False):
        
        print ("##### _lead_create_contact [START] #####")
        
        #Nomes dos campos a serem separados e preenchidos.
        
        #key_word = ["cnpj_cpf : ", "inscr_est : ", "zip : ", "street : ", "number : ", "street2 : ", "district : ", "country_id : ", "state_id : ", "city_id : "]

        key_word = ["company_type : ", "cnpj_cpf : ", "zip : ", "street : ", "number : ", "street2 : ", "district : ", "country_id : ", "state_id : ", "city_id : "]

        table_infos = []
        
        custom_infos = self.description
        
        if not isinstance(custom_infos, bool):
            custom_infos = custom_infos.replace("\n", " ")

            #Adiciona o campo inscr_est caso seja uma pessoa jurídica, e altera os campos a serem separados.
            if "company_type : person" not in custom_infos:
                key_word.insert(2, "inscr_est : ")
                                
                FIELDS_QTY = 11
            else:
                FIELDS_QTY = 10;
            
            for x in range(FIELDS_QTY):

                if x < len(key_word)-1:
                    matches = re.compile(".*" + key_word[x] + "" + ".*\s" + key_word[x+1]).match(custom_infos)
                else:
                    matches = re.compile(".*" + key_word[x] + "" + ".*").match(custom_infos)

                temp = re.sub(".*" + key_word[x], "", matches.group())

                if x < len(key_word)-1:
                    temp = re.sub(key_word[x+1], "", temp)

                table_infos.append(temp)

        """
        table_infos
        0 | cnpj_cpf,
        1 | inscr_est,
        2 | zip,
        3 | street,
        4 | number,
        5 | street2,
        6 | district,
        7 | country_id,
        8 | state_id,
        9 | city_id
        """
        
        email_split = tools.email_split(self.email_from)
        
        if not is_company:
            values = {
                'name': name,
                'user_id': self.env.context.get('default_user_id') or self.user_id.id,
                'comment': self.description,
                'team_id': self.team_id.id,
                'parent_id': parent_id,
                'phone': self.phone,
                'mobile': self.mobile,
                
                #'email': email_split[0] if email_split else False,
                
                'fax': self.fax,
                'title': self.title.id,
                'function': self.function,
                
                'street': self.street,
                'street2': self.street2,
                'zip': self.zip,
                'city': self.city,
                'country_id': self.country_id.id,
                'state_id': self.state_id.id,
                'is_company': is_company,
                'type': 'contact'
            }
        
        if is_company:
            if "company" in table_infos[0]:
                custom_country = self.env['res.country'].search([('id','=', int(table_infos[8]))])
                
                custom_state = self.env['res.country.state'].search([('id','=', int(table_infos[9]))])
                
                custom_city = self.env['res.state.city'].search([('id','=', int(table_infos[10]))])
                
                #self.cnpj = table_infos[0]
                
                #self.inscr_est = table_infos[1]
                
                values = {
                    'name': name,
                    'user_id': self.env.context.get('default_user_id') or self.user_id.id,
                    'comment': self.description,
                    'team_id': self.team_id.id,
                    'parent_id': parent_id,
                    'phone': self.phone,
                    'mobile': self.mobile,
                    
                    'email': email_split[0] if email_split else False,
                    
                    'fax': self.fax,
                    'title': self.title.id,
                    'function': self.function,
                    
                    'cnpj_cpf': table_infos[1],
                    'inscr_est': table_infos[2],
                    'zip': table_infos[3],
                    'street': table_infos[4],
                    'number': table_infos[5],
                    'street2': table_infos[6],
                    'district': table_infos[7],
                    
                    'city_id': custom_city.id,
                    'country_id': custom_country.id,
                    'state_id': custom_state.id,
                    #'zip': self.zip,
                    'is_company': is_company,
                    'type': 'contact'
                }
            elif "person" in table_infos[0]:
                custom_country = self.env['res.country'].search([('id','=', int(table_infos[7]))])
                
                custom_state = self.env['res.country.state'].search([('id','=', int(table_infos[8]))])
                
                custom_city = self.env['res.state.city'].search([('id','=', int(table_infos[9]))])
                
                #self.cnpj = table_infos[0]
                
                #self.inscr_est = table_infos[1]
                
                values = {
                    'name': name,
                    'user_id': self.env.context.get('default_user_id') or self.user_id.id,
                    'comment': self.description,
                    'team_id': self.team_id.id,
                    'parent_id': parent_id,
                    'phone': self.phone,
                    'mobile': self.mobile,
                    
                    'email': email_split[0] if email_split else False,
                    
                    'fax': self.fax,
                    'title': self.title.id,
                    'function': self.function,
                    
                    'cnpj_cpf': table_infos[1],
                    #'inscr_est': table_infos[2],
                    'zip': table_infos[2],
                    'street': table_infos[3],
                    'number': table_infos[4],
                    'street2': table_infos[5],
                    'district': table_infos[6],
                    
                    'city_id': custom_city.id,
                    'country_id': custom_country.id,
                    'state_id': custom_state.id,
                    #'zip': self.zip,
                    'is_company': False,
                    'type': 'contact'
                }
        
        print ("##### _lead_create_contact [END] #####")
    
        return self.env['res.partner'].create(values)
    
    @api.multi
    def _convert_opportunity_data(self, action, customer, team_id=False):
        print ("##### _convert_opportunity_data [START] #####")
        
        if not team_id:
            team_id = self.team_id.id if self.team_id else False
        value = {
            'planned_revenue': self.planned_revenue,
            'probability': self.probability,
            'name': self.name,
            'partner_id': customer.id if customer else False,
            'type': 'opportunity',
            'date_open': fields.Datetime.now(),
            'email_from': customer and customer.email or self.email_from,
            'phone': customer and customer.phone or self.phone,
            'date_conversion': fields.Datetime.now(),
        }
        if not self.stage_id:
            stage = self._stage_find(team_id=team_id)
            value['stage_id'] = stage.id
            if stage:
                value['probability'] = stage.probability
        
        if action == 'create_both':
        
            print ("##### create_user [START] #####")
            
            user = self.env['res.users']
            
            partner = self.env['res.partner'].browse(value.get('partner_id'))
                    
            vals = {
                'active': True,
                'login': value.get('email_from'),
                'partner_id': partner.parent_id.id,
                'share': False,
                'alias_id': 1,
                'sale_team_id': 1,
                #'password': "teste",
                #'partner_id': value.get('partner_id'),
            }
            
            user.create(vals)
            
            print ("##### groups_write [START] #####")
        
            user = self.env['res.users'].search([('login','=', vals['login'])])
            
            groups_remove_acess = [1, 3, 4, 8, 11, 12, 13, 15, 16, 21, 22, 23, 24, 25, 26, 27, 46, 47, 58]
            
            groups_grant_acess = [9]
            
            for x in groups_remove_acess:
                group = self.env['res.groups'].search([('id','=', x)])

                group.write({'users': [(3, user.id)]})
            
            for y in groups_grant_acess:
                group = self.env['res.groups'].search([('id','=', y)])
            
                group.write({'users': [(4, user.id)]})
            
            print ("##### groups_write [END] #####")
            
            print ("##### create_user [END] #####")
        
        print ("##### _convert_opportunity_data [END] #####")
       
        return value
    
    
    @api.multi
    def convert_opportunity(self, action, partner_id, user_ids=False, team_id=False):
        print ("##### convert_opportunity [START] #####")
        
        customer = False
        
        if partner_id:
            customer = self.env['res.partner'].browse(partner_id)
        for lead in self:
            if not lead.active or lead.probability == 100:
                continue
            vals = lead._convert_opportunity_data(action, customer, team_id)
            lead.write(vals)

        if user_ids or team_id:
            self.allocate_salesman(user_ids, team_id)

        print ("##### convert_opportunity [END] #####")
        
        return True
    
class Lead2OpportunityMassConvert(models.TransientModel):
    _inherit = 'crm.partner.binding'

    action = fields.Selection([
        ('create_both', 'Create a new customer with user'),
        ('create', 'Create a new customer without user'),
    ], 'Related Customer', required=True, default=lambda self: self._context.get('action', 'create_both'))

    """
    action = fields.Selection([
        ('create_both', 'Create a new customer with user'),
        ('exist', 'Link to an existing customer'),
        ('create', 'Create a new customer'),
        ('nothing', 'Do not link to a customer')
    ], 'Related Customer', required=True)
    """
    
    #####
    
class Lead2OpportunityMassConvert(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    name = fields.Selection([
        ('convert', 'Convert to opportunity'),
    ], 'Conversion Action', required=True)

    @api.multi
    def _convert_opportunity(self, vals):
        print ("##### _convert_opportunity [ACTION] [START] #####")

        
        
        self.ensure_one()

        res = False

        leads = self.env['crm.lead'].browse(vals.get('lead_ids'))
        for lead in leads:
            self_def_user = self.with_context(default_user_id=self.user_id.id)
            partner_id = self_def_user._create_partner(
                lead.id, self.action, vals.get('partner_id') or lead.partner_id.id)
            res = lead.convert_opportunity(self.action, partner_id, [], False)
        user_ids = vals.get('user_ids')

        leads_to_allocate = leads
        if self._context.get('no_force_assignation'):
            leads_to_allocate = leads_to_allocate.filtered(lambda lead: not lead.user_id)

        if user_ids:
            leads_to_allocate.allocate_salesman(user_ids, team_id=(vals.get('team_id')))

        print ("##### _convert_opportunity [ACTION] [END] #####")
        
        return res
    
    #####
    
    """
    
    #####
    
    #Params: res.groups.write()
    
    #####
    
    0, 0, { values }) link to a new record that needs to be created with the given values dictionary

    (1, ID, { values }) update the linked record with id = ID (write values on it)

    (2, ID) remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)

    (3, ID) cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)

    (4, ID) link to existing record with id = ID (adds a relationship)

    (5) unlink all (like using (3,ID) for all linked records)

    (6, 0, [IDs]) replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
    
    #####
    
    """