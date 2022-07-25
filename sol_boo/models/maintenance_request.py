from odoo import _, api, fields, models

class ActionPlanMaintenance(models.Model):
    _name = 'action.plan.maintenance'
    _description = 'Action Plan Maintenance'
    
    name = fields.Char('Plan')
    due_date = fields.Datetime('Due Date')
    status = fields.Selection([
        ('open', 'Open'),
        ('op', 'On Progress'),
        ('done', 'Done'),
    ], string='status',default="open")
    maintenance_id = fields.Many2one('maintenance.request', string='Maintenance')


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    _description = 'Maintenance Request'
    
    action_plan_line = fields.One2many('action.plan.maintenance', 'maintenance_id', string='Action Plan')

