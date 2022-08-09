# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    name_project = fields.Char(string='Name Project')
    need_category = fields.Selection([
        ('project', 'Project'),
        ('operational', 'Operational'),
        ('maintenance', 'Maintenance'),
        ('trading', 'Trading'),
        ('bidding', 'Bidding')
    ], string='Need Category')
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase.requisition.req')
        return super(PurchaseRequisition, self).create(vals)

class DeliveryLocation(models.Model):
    _name = 'delivery.location'
    _description = 'Delivery Location'

    name = fields.Char(string='Delivery Location')

class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    merk_recommended = fields.Char(string='Merk Recommended')
    price_target = fields.Float('Price Target')
    date_plan_required = fields.Date('Date Plan Required')
    delivery_location_id = fields.Many2one(string='Delivery Location', comodel_name='delivery.location', ondelete='restrict')
    product_description_variants = fields.Text(string='Custom Description', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            product_description_variants = ''
            # if self.product_id.code:
            #     product_description_variants = "[{}] {}".format(self.product_id.default_code, product_description_variants)
            if self.product_id.type_pur:
                product_description_variants += "type : " + self.product_id.type_pur + ";"
            if self.product_id.debit:
                product_description_variants += "\n" + "debit : " + self.product_id.debit + ";"
            if self.product_id.head:
                product_description_variants += "\n" + "head : " + self.product_id.head + ";"
            if self.product_id.voltage:
                product_description_variants += "\n" + "voltage : " + self.product_id.voltage + ";"
            if self.product_id.casing:
                product_description_variants += "\n" + "material casing : " + self.product_id.casing + ";"
            if self.product_id.impeller:
                product_description_variants += "\n" + "material impeller : " + self.product_id.impeller + ";"
            self.product_uom_id = self.product_id.uom_id.id
            self.product_description_variants = product_description_variants

class ProductProduct(models.Model):
    _inherit = 'product.product'

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type_pur = fields.Char(string='Type')
    debit = fields.Char(string='Debit')
    head = fields.Char(string='Head')
    voltage = fields.Char(string='Voltage')
    casing = fields.Char(string='Casing')
    impeller = fields.Char(string='Impeller')

class PurchaseOrderLine(models.Model):
    _inherit ='purchase.order.line'

    project_code = fields.Char(string='Project Code')

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char(string='Order Reference')
    notes = fields.Html(string='Notes')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.req')
        return super(PurchaseOrder, self).create(vals)
