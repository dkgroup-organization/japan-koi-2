# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class SimpleProductBrand(models.Model):
    _name = 'simple.product.brand'

    name = fields.Char(
        string='Brand Name',
        required=True)
    description = fields.Text(
        string='Description',
        translate=True)
    image = fields.Binary(
        string='Logo File')
    brand_products = fields.One2many(
        'product.template',
        'simple_product_brand_id',
        string='Related Products',)
    brand_products_count = fields.Integer(
        string='#Products',
        compute='_compute_brand_product_count',
    )

    #@api.one
    @api.depends('brand_products')
    def _compute_brand_product_count(self):
        self.brand_products_count = len(self.brand_products)


