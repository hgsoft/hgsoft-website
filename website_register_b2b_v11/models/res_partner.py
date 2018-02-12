from openerp import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
class ResPartner(models.Model):
    _inherit = 'crm.lead'
    
    @api.multi
    def _convert_opportunity_data(self, customer, team_id=False):
        print ("##### _convert_opportunity_data [START] #####")
    
    
        user = self.env['res.users'].search([('login','=', vals['login'])])

        print ("##### _convert_opportunity_data [END] #####")
        
        return value
