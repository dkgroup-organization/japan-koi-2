# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare

class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    price = fields.Float(digits="Product Supplier Decimal")

class ProductProduct(models.Model):
    #_name = 'product.product'
    _inherit = 'product.product'

    standard_price = fields.Float(digits="Product Supplier Decimal")

class ProductTemplate(models.Model):
    #_name = 'product.template'
    _inherit = 'product.template'

    standard_price = fields.Float(digits="Product Supplier Decimal")


