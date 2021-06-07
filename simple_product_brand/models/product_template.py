# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    simple_product_brand_id = fields.Many2one(
        'simple.product.brand',
        string='Brand',
        help='Select your brand'
    )



