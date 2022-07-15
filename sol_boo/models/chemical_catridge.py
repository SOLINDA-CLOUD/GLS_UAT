from odoo import _, api, fields, models

class ChemicalCatridge(models.Model):
    _name = 'chemical.catridge'
    _description = 'Chemical Catridge'
    

    product_id = fields.Many2one('product.product', string='Product/Chemical')
    date = fields.Date('Date',default=fields.Date.today)
    stock_awal = fields.Float('Stock Awal')
    penerimaan = fields.Float('Penerimaan')
    penuangan = fields.Float(string='Penuangan')
    pemakaian = fields.Float(string='Pemakaian')
    cleaning_basa = fields.Float('Pemakaian Cleaning Basa')
    adj_over_loss = fields.Float('Adjustment Over/(Loss)')
    dosing_stroke = fields.Float('Dosing Stoke')
    sisa_stock = fields.Float(compute='_compute_sisa_stock', string='Sisa Stock')
    
    @api.depends('stock_awal','penerimaan','penuangan','pemakaian','cleaning_basa','adj_over_loss','dosing_stroke')
    def _compute_sisa_stock(self):
        for i in self:
            i.sisa_stock = i.stock_awal or 0 + i.penerimaan or 0 - i.penuangan or 0 - i.pemakaian or 0 - i.cleaning_basa or 0 - i.adj_over_loss or 0 - i.dosing_stroke or 0

    