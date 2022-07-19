from odoo import _, api, fields, models
from datetime import datetime,date

class ShutdownSystem(models.Model):
    _name = 'shutdown.system'
    _description = 'Shutdown System'
    
    time = fields.Datetime('Waktu', default=datetime.now())
    notes = fields.Text('Keterangan')
    jadwal_pelaksana = fields.Date('Jadwal Pelaksanaan')
    type = fields.Selection([
        ('trouble', 'Input Trouble'),
        ('cleaning', 'Request Cleaning'),
        ('backwash', 'Backwash'),
        ('grease', 'Request Grease')
    ], string='type')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('req', 'Requested'),
        ('approve', 'Approved'),
    ], string='Status',default="draft")
    attachment = fields.Binary('Attachment')
    filename = fields.Char('File Name')
    request_id = fields.Many2one('res.users', string='Requested By')
    approve_id = fields.Many2one('res.users', string='Approved By')
    job_order_id = fields.Many2one('job.order.request', string='Job Order')
    water_prod_id = fields.Many2one('water.prod.daily', string='Water Production')
    warehouse_id = fields.Many2one('stock.warehouse', string='Lokasi',related="water_prod_id.warehouse_id")
    
    def open_self_record(self):
        return {
                    'name': 'Request',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'shutdown.system',
                    'res_id': self.id,
                    'context': {'create': False}
                }

    def create_open_job_order(self):
        for i in self:
            i.ensure_one()
            if i.job_order_id:
                return {
                        'name': 'Job Order Request',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'job.order.request',
                        'res_id': i.job_order_id.id,
                        'context': {'create': False}
                    }
            else:
                job_order = self.env["job.order.request"].create({
                            'state': 'draft',
                            'warehouse_id': i.warehouse_id.id,
                            'problem': i.notes,
                            })
                if job_order:
                    i.job_order_id = job_order.id
                    return {
                    'name': 'Job Order Request',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'job.order.request',
                    'res_id': job_order.id,
                    }


class WaterProdDaily(models.Model):
    _name = 'water.prod.daily'
    _description = 'Water Prod Daily'
    _inherit = 'mail.thread'

    # IRISAN
    name = fields.Char('Name',tracking=True)
    date = fields.Date('Date',default=fields.Date.today,tracking=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Lokasi',tracking=True)

    # HARIAN
    laguna = fields.Char('Laguna',tracking=True)
    target_prod = fields.Integer('Target Produksi',tracking=True)
    kontrak_boo = fields.Integer('Berdasarkan Kontrak BOO',default=450,tracking=True)
    adjustment_prod = fields.Integer('Penyesuaian Produksi',tracking=True)
    adendum = fields.Integer('Adendum',tracking=True)
    now_prod = fields.Float('Produksi Sekarang',tracking=True)
    over_target = fields.Float('Produksi Melebihi Target',compute="_compute_over_target",store=True,tracking=True)
    freq_hpp = fields.Integer('Frekuensi HPP',tracking=True)
    flow_prod = fields.Integer('Flow Produksi',tracking=True)
    catatan = fields.Text('Catatan',tracking=True)

    # PEKANAN DAN BULANAN
    aktual_ro = fields.Float('Konsumsi Aktual Ro(m3)',tracking=True)
    lwbp = fields.Integer('LWBP',tracking=True)
    lwbp_real = fields.Float('LWBP Real',tracking=True)
    wbp = fields.Integer(string='WBP',tracking=True)
    wbp_real = fields.Float('WBP Real',tracking=True)
    sec = fields.Float('Seconds',tracking=True)
    minimum_prod = fields.Float('Minimum Produksi',tracking=True)
    hasil_prod = fields.Float('Hasil Produksi',tracking=True)
    remarks = fields.Text('Remarks',tracking=True)
    water_prod_id = fields.Many2one('water.prod.daily', string='water_prod',tracking=True)

    # LINE
    shutdown_system_line = fields.One2many('shutdown.system', 'water_prod_id', string='Shutdown System')

    def _compute_over_target(self):
        for i in self:
            if i.target_prod and i.now_prod:
                i.over_target = i.now_prod - i.target_prod
            else:
                i.over_targer = 0

    @api.model
    def create(self, vals):
        res = super(WaterProdDaily, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("wpd.seqcode")
        return res 