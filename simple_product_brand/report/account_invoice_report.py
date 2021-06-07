# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import tools, models, fields, api

class AccountMoveReport(models.Model):
    _inherit = 'account.move.report'

    simple_product_brand_id = fields.Many2one(
        comodel_name='simple.product.brand',
        string='Brand', readonly=True)

    def _select(self):
        return super(AccountInvoiceReport, self)._select(
        ) + " , sub.simple_product_brand_id as simple_product_brand_id"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select(
        ) + " , pt.simple_product_brand_id as simple_product_brand_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by(
        ) + " , pt.simple_product_brand_id"