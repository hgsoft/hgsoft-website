from openerp import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.multi
    def _convert_opportunity_data(self, customer, team_id=False):
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
        
        print ("##### create_user [START] #####")
        
        user = self.env['res.users']
        
        vals = {
            'active': True,
            'login': value.get('email_from'),
            'password': "teste",
            'partner_id': value.get('partner_id'),
            'share': False,
            'alias_id': 1,
            'sale_team_id': 1,
            
            #active, login, password, company_id, partner_id,
            #share, alias_id, sale_team_id
            
        }
        
        user.create(vals)
        
        print ("##### create_user [END] #####")
        
        print ("##### _convert_opportunity_data [END] #####")
        
        return value
    
    
    @api.multi
    def convert_opportunity(self, partner_id, user_ids=False, team_id=False):
        print ("##### convert_opportunity [START] #####")
        
        customer = False
        
        if partner_id:
            customer = self.env['res.partner'].browse(partner_id)
        for lead in self:
            if not lead.active or lead.probability == 100:
                continue
            vals = lead._convert_opportunity_data(customer, team_id)
            lead.write(vals)

        if user_ids or team_id:
            self.allocate_salesman(user_ids, team_id)

        print ("##### convert_opportunity [END] #####")
        
        return True

class Lead2OpportunityMassConvert(models.TransientModel):
    _inherit = 'crm.partner.binding'
    
    action = fields.Selection([
        ('exist', 'Link to an existing customer'),
        ('create', 'Create a new customer'),
        ('create_both', 'Create a new customer and user'),
        ('nothing', 'Do not link to a customer')
    ], 'Related Customer', required=True)