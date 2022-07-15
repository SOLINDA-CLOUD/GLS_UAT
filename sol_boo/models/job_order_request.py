from odoo import _, api, fields, models

class ApprovalJobOrder(models.Model):
    _name = 'approval.job.order'
    _description = 'Approval Job Order'
    
    type = fields.Selection([('request', 'Requested By'), ('reviewed', 'Reviewed By'),('approved', 'Approved By')], string='type')
    user_id = fields.Many2one('res.users', string='Name')  
    date = fields.Date('Date')
    job_order_id = fields.Many2one('job.order.request', string='Job Order') 


class JobOrderRequest(models.Model):
    _name = 'job.order.request'
    _description = 'Job Order Request'
    _inherit = 'mail.thread'

    name = fields.Char('Job Order No',tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('req', 'Requested'),
        ('review', 'Reviewed'),
        ('approve', 'Approved'),
    ], string='State',default='draft')
    location = fields.Char('Location',tracking=True)
    problem = fields.Text('Problem(Permasalahan)',tracking=True)
    root_cause = fields.Text('Root Cause (Penyebab)',tracking=True)
    action_taken = fields.Text('Action Taken(Tindakan)',tracking=True)
    # BEFORE MAINTENANCE
    approval_line = fields.One2many('approval.job.order', 'job_order_id', string='Approval')
    subcontractor_id = fields.Many2one('res.partner', string='Subcontractor')
    main_hours = fields.Float('Main Hours')
    before_maintenance_date = fields.Date('Date')
    # AFTER MAINTENANCE
    turned_over_id = fields.Many2one('res.users', string='Turned Over By')
    turned_over_datetime = fields.Datetime('Datetime of Turned Over')
    accepted_id = fields.Many2one('res.users', string='Accepted By')
    accepted_datetime = fields.Datetime('Datetime Job Complated')
    note = fields.Text('Note',tracking=True)

    def update_line_approval(self,code):
        return (0,0,{
                'type':code,
                'user_id':self.env.user.id,
                'date':fields.date.today(),
            })

    def set_to_draft(self):
        for i in self:
            i.state = 'draft'
            i.approval_line = [5,0,0]


    def submit_jor(self):
        for i in self:
            i.state = 'req'
            i.approval_line = [i.update_line_approval('request')]

    def review_jor(self):
        for i in self:
            i.state = 'review'
            i.approval_line = [i.update_line_approval('reviewed')]

    def approve_jor(self):
        for i in self:
            i.state = 'approve'
            i.approval_line = [i.update_line_approval('approved')]
        
    @api.model
    def create(self, vals):
        res = super(JobOrderRequest, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("jor.seqcode")
        return res 
