# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import tools, models, fields, api

class SaleReport(models.Model):
    _inherit = 'sale.report'

    simple_product_brand_id = fields.Many2one(
        comodel_name='simple.product.brand',
        string='Brand', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['simple_product_brand_id'] = ", t.simple_product_brand_id as simple_product_brand_id"
        groupby += " , t.simple_product_brand_id"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)