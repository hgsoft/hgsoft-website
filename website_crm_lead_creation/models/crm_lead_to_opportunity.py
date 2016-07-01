# coding=utf-8
'''
Created on 06/08/2015

@author: danimar
'''
from openerp import models, fields, api


class crm_lead2opportunity_partner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    create_user = fields.Boolean(string="Criar usuário", default=True)
    send_mail = fields.Boolean(string="Enviar e-mail", default=True)

    @api.model
    def _create_partner(self, lead_id, action, partner_id, context=None):
        context = dict(self.env.context or {})
        context.update({'create_user': self.create_user,
                   'send_email': self.send_mail})
        self = self.with_context(context)
        super(crm_lead2opportunity_partner, self)._create_partner(
            lead_id, action, partner_id, context=context)
