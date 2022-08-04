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
    shutdown_id = fields.Many2one('shutdown.system', string='Shutdown')
    job_order_id = fields.Many2one('job.order.request', string='Job Order') 
    
    mr_ids = fields.One2many('stock.picking', 'maintenance_id', string='MR')
    mr_count = fields.Integer(compute='_compute_mr_count', string='MR')


    @api.depends('mr_ids')
    def _compute_mr_count(self):
        for i in self:
            i.mr_count = len(i.mr_ids)

    def create_open_mr(self):
         return {
                'name': 'Material Request',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,kanban,form,calendar,map',
                'res_model': 'stock.picking',
                'context': {'default_company_id': self.env.company.id,'default_maintenance_id':self.id},
                'domain': [('maintenance_id','=',self.id)],
            }
