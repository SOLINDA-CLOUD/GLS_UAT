from odoo import models, fields, api

class AccountPayment(models.TransientModel):
    _inherit = 'account.payment.register'

    other_costs = fields.Monetary(string='Additional Other Costs')
    other_account = fields.Many2one('account.account', string='Additional Account', ondelete='cascade')