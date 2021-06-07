# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import tools, models, fields, api

class PurchaseReport(models.Model):
    _inherit = 'purchase.report'

    simple_product_brand_id = fields.Many2one(
        comodel_name='simple.product.brand',
        string='Brand', readonly=True)

    def _select(self):
        return super(PurchaseReport, self)._select(
        ) + " , t.simple_product_brand_id as simple_product_brand_id"

    def _group_by(self):
        return super(PurchaseReport, self)._group_by(
        ) + " , t.simple_product_brand_id"
