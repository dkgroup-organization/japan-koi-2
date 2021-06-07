# -*- coding: utf-8 -*-
#############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import random
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta, datetime, date, time
from odoo.addons.prestashop_connector_gt.prestapyt.prestapyt import PrestaShopWebServiceError as PrestaShopWebServiceError
from odoo.addons.prestashop_connector_gt.prestapyt.prestapyt import PrestaShopWebService as PrestaShopWebService
from odoo.addons.prestashop_connector_gt.prestapyt.prestapyt import PrestaShopWebServiceDict as PrestaShopWebServiceDict

class account_invoice(models.Model):
    _inherit = "account.move"
                
    is_prestashop=fields.Boolean('Prestashop')
    total_discount_tax_excl=fields.Float('Discount(tax excl.)')
    total_discount_tax_incl=fields.Float('Discount(tax incl)')
    total_paid_tax_excl= fields.Float('Paid (tax excl.)')
    total_paid_tax_incl=fields.Float('Paid (tax incl.)')
    total_products_wt=fields.Float('Weight')
    total_shipping_tax_excl=fields.Float('Shipping(tax excl.)')
    total_shipping_tax_incl=fields.Float('Shipping(tax incl.)')
    total_wrapping_tax_excl=fields.Float('Wrapping(tax excl.)')
    total_wrapping_tax_incl=fields.Float('Wrapping(tax incl.)')
    shop_ids = fields.Many2many('sale.shop', 'invoice_shop_rel', 'invoice_id', 'shop_id', string="Shop")

    def invoice_pay_customer_base(self):
        accountinvoice_link = self
        journal_id = self._default_journal()

        if self.type == 'out_invoice':
            self.with_context(type='out_invoice')
        elif self.type == 'out_refund':    
            self.with_context(type='out_refund')
        self.pay_and_reconcile(journal_id,accountinvoice_link.amount_total, False, False)
        return True    

    def _is_prestashop_invoice(self):
        if self.invoice_origin and self.move_type == 'out_invoice':
            sale_orders = self.env['sale.order'].sudo().search([('name', '=', self.invoice_origin),('presta_id', '!=', False)])
            if sale_orders:
                return True
        return False

    def _get_last_sequence_from_prestashop(self):
        sale_orders = self.env['sale.order'].sudo().search([('name', '=', self.invoice_origin),('presta_id', '!=', False)])
        for sale_order in sale_orders:
            try:
                if self.name == '/':
                    prestashop = PrestaShopWebServiceDict(sale_order.shop_id.prestashop_instance_id.location,sale_order.shop_id.prestashop_instance_id.webservice_key or None)
                    if prestashop.get('orders',sale_order.presta_id):
                        order_detail = prestashop.get('orders',sale_order.presta_id)
                        order_data_ids = order_detail.get('order')
                        if order_data_ids:
                            invoice_num = order_data_ids.get('invoice_number')
                            if invoice_num and not str(invoice_num) == "1" and not str(invoice_num) == "0":
                                invoice_num = int(invoice_num) - 1
                                dinvoice = order_data_ids.get('invoice_date')
                                if dinvoice and  '0000-00-00' not in dinvoice:
                                    date_obj = datetime.strptime(dinvoice, '%Y-%m-%d %H:%M:%S')
                                    self.invoice_date = date_obj
                                    self.invoice_date_due = date_obj
                                    self.amount_untaxed = sale_order.amount_untaxed
                                    self.amount_total = sale_order.amount_total
                                    self.amount_residual = sale_order.amount_total
                                return "%s%06d" % ("FA", invoice_num)
            except:
                pass
        return False

    def _get_last_sequence(self, relaxed=False):
        res = super()._get_last_sequence(relaxed=relaxed)
        if self._is_prestashop_invoice():
            presta = self._get_last_sequence_from_prestashop()
            if presta:
                res = presta
        return res

    def _get_last_sequence_domain(self, relaxed=False):
        where_string, param = super(account_invoice, self)._get_last_sequence_domain(relaxed)
        sale_orders = self.env['sale.order'].sudo().search([('name', '=', self.invoice_origin),('presta_id', '!=', False)])
        if sale_orders and self.move_type == 'out_invoice':
            where_string += " AND (length(name) = 8 OR  is_prestashop IS TRUE) "
        else:
            where_string += " AND length(name) > 8 AND is_prestashop IS NOT TRUE "
        return where_string, param

account_invoice()