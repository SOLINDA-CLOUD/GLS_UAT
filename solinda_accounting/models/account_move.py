from itertools import product
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.constrains('ref')
    def _check_mobile_unique(self):
        if self.ref:
            ref_counts = self.search_count(
                [('ref', '=', self.ref), ('id', '!=', self.id)])
            print(self.ref)
            if ref_counts > 0:
                raise ValidationError("Reference number already exists!")
        else:
            return

    @api.depends('invoice_line_ids.qty_received_account')
    def _compute_total_qty_received(self):
        for this in self:
            this.total_qty_received = sum(
                this.invoice_line_ids.mapped('qty_received_account'))

    @api.depends('invoice_line_ids.product_id')
    def _compute_total_qty_ordered(self):
        for this in self:
            this.total_qty_ordered = sum(
                this.invoice_line_ids.mapped('qty_ordered_account'))

    @api.depends('invoice_line_ids.detailed_type')
    def _compute_product_type(self):
        label = dict(self._fields['detailed_type'].selection)
        for this in self:
            product = ''
            for lines in this.invoice_line_ids:
                if '%s, ' % label.get(lines.detailed_type) in product:
                    continue
                else:
                    product += '%s, ' % label.get(lines.detailed_type)
            this.product_type = product

    @api.depends('invoice_line_ids.qty_delivered_account')
    def _compute_total_delivered_qty(self):
        for this in self:
            this.total_delivered_qty = sum(
                this.invoice_line_ids.mapped('qty_delivered_account')
            )
    
    total_qty_received = fields.Integer(compute='_compute_total_qty_received', string='Qty Received', store=True)

    total_qty_ordered = fields.Integer(compute='_compute_total_qty_ordered', string='Qty Ordered', store=True)
    invoice_line_ids = fields.One2many('account.move.line', 'move_id', string='Invoice lines',
                                       copy=False, readonly=True,
                                       domain=[
                                           ('exclude_from_invoice_tab', '=', False)],
                                       states={'draft': [('readonly', False)]})

    product_type = fields.Text(compute='_compute_product_type', string='Product Type')
    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product')], string='Product Type', default='consu', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')

    total_delivered_qty = fields.Integer(compute='_compute_total_delivered_qty', string='Qty Delivered', store=True)
  

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    purchase_line_id = fields.Many2one(
        'purchase.order.line', 'Purchase Order Line', ondelete='set null', index=True)
    qty_received_account = fields.Float(related='purchase_line_id.qty_received', store=True, string="Qty Received")
    qty_ordered_account = fields.Float(related='purchase_line_id.product_qty', store=True, string="Qty Ordered")
    product_id = fields.Many2one(
        'product.product', string='Product', ondelete='restrict')
    detailed_type = fields.Selection(related='product_id.detailed_type', string='Product Type')

    sale_order_line = fields.Many2one('sale.order.line', string='Order Lines', ondelete='set null', index=True)
    qty_delivered_account = fields.Float(compute='_compute_delivered', string='Qty Delivered', store=True)
    
    @api.depends('sale_order_line')
    def _compute_delivered(self):
        if self.sale_order_line:
            self.qty_delivered_account = self.sale_order_line.qty_delivered  

