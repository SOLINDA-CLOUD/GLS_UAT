from odoo import _, api, fields, models


class OperationBoo(models.Model):
    _name = 'operation.boo'
    _description = 'Operation Boo'
    
    name = fields.Char('Name')
    warehouse_id = fields.Many2one('stock.warehouse', string='Location',related="water_prod_id.warehouse_id")
    date = fields.Date('Date', default=fields.Date.today)
    aktual_ro = fields.Float('Konsumsi Aktual Ro(m3)')
    lwbp = fields.Integer('LWBP')
    lwbp_real = fields.Float('LWBP Real')
    wbp = fields.Integer(string='WBP')
    wbp_real = fields.Float('WBP Real')
    sec = fields.Float('Seconds')
    minimum_prod = fields.Float('Minimum Produksi')
    # hasil_prod = fields.Float('Hasil Produksi')
    remarks = fields.Text('Remarks')
    water_prod_id = fields.Many2one('water.prod.daily', string='water_prod')

class WaterProdDaily(models.Model):
    _name = 'water.prod.daily'
    _description = 'Water Prod Daily'
    
    date = fields.Date('Date',default=fields.Date.today)
    warehouse_id = fields.Many2one('stock.warehouse', string='Lokasi')
    laguna = fields.Char('Laguna')
    target_prod = fields.Integer('Target Produksi')
    adjustment_prod = fields.Integer('Penyesuaian Produksi')
    adendum = fields.Integer('Adendum')
    now_prod = fields.Float('Produksi Sekarang')
    over_target = fields.Float('Produksi Melebihi Target',compute="_compute_over_target",store=True)
    freq_hpp = fields.Integer('Frekuensi HPP')
    flow_prod = fields.Integer('Flow Produksi')
    catatan = fields.Text('Catatan')

    operation_line = fields.One2many('operation.boo', 'water_prod_id', string='Operations')

    def _compute_over_target(self):
        for i in self:
            if i.target_prod and i.now_prod:
                i.over_target = i.now_prod - i.target_prod
            else:
                i.over_targer = 0

    # @api.model
    # def create(self, vals):
    #     res = super(WaterProdDaily, self).create(vals)
    #     res.name = self.env["ir.sequence"].next_by_code("waterprod.seq")
    #     return res 