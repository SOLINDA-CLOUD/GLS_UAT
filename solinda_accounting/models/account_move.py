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


    total_delivered_qty = fields.Integer(compute='_compute_total_delivered_qty', string='Qty Delivered', store=True)
    total_qty_received = fields.Integer(
        compute='_compute_total_qty_received', string='Qty Received', store=True)
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
    

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    purchase_line_id = fields.Many2one(
        'purchase.order.line', 'Purchase Order Line', ondelete='set null', index=True)
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', ondelete='set null', index=True)
    qty_received_account = fields.Float(related='purchase_line_id.qty_received', store=True, string="Qty Received")
    product_id = fields.Many2one(
        'product.product', string='Product', ondelete='restrict')
    detailed_type = fields.Selection(related='product_id.detailed_type', string='Product Type')
    qty_delivered_account = fields.Float(related='sale_order_line_id.qty_delivered', store=True, string='Qty Delivered')