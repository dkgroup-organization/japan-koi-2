# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)

class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    applied_on = fields.Selection(selection_add=[
        ('5_brand', 'Product Brand')], default='3_global', required=True, ondelete={'5_brand': 'cascade'})

    simple_product_brand_id = fields.Many2one(
        comodel_name="simple.product.brand", string="Brand")

    def _get_pricelist_item_name_price(self):
        super(ProductPricelistItem, self)._get_pricelist_item_name_price()
        for rec in self:
            if rec.simple_product_brand_id:
                rec.name = _("Brand: %s") % (rec.simple_product_brand_id.name)
