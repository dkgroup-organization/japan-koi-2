# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DkgImportProductVariantTemplate(models.Model):
    _name = 'dkg.import.product.variant.template'
    _description = 'import product variant template'

    ## TEMPLATE FIELDS

    external_id = fields.Char('External ID')
    name = fields.Char('Name')
    type = fields.Selection([('consu', 'Consumable'), ('service', 'Service'), ('product', 'Storable Product'), ],
                            string='Product Type')
    sale_ok = fields.Boolean('Can be Sold', )
    purchase_ok = fields.Boolean('Can be Purchased', )
    taxes_id = fields.Many2many('account.tax', 'product_templ_taxes_rel', 'prod_templ_id', 'tax_id', help="Default taxes used when selling the product.",
        string='Customer Taxes',
        domain=[('type_tax_use', '=', 'sale')])
    supplier_taxes_id = fields.Many2many('account.tax', 'product_templ_supplier_taxes_rel', 'prod_templ_id', 'tax_id', string='Vendor Taxes',
        help='Default taxes used when buying the product.',
        domain=[('type_tax_use', '=', 'purchase')])
    invoice_policy = fields.Selection([('order', 'Ordered quantities'), ('delivery', 'Delivered quantities')],
                                      string='Invoicing Policy', )
    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure', )
    uom_po_id = fields.Many2one(
        'uom.uom', 'Purchase Unit of Measure', )
    active = fields.Boolean(
        'Active', default=True)
    description_sale = fields.Text('Sales Description')
    default_code = fields.Char('Internal Reference')
    barcode = fields.Char('Barcode')

    weight = fields.Float('Weight', digits='Stock Weight')
    standard_price = fields.Float('Cost', digits='Product Price')
    fix_price = fields.Float(string='Fix Price')

    category_level_0 = fields.Char(string="Category Level 0", required=False, )
    category_level_1 = fields.Char(string="Category Level 1", required=False, )
    category_level_2 = fields.Char(string="Category Level 2", required=False, )
    category_level_3 = fields.Char(string="Category Level 3", required=False, )
    category_level_4 = fields.Char(string="Category Level 4", required=False, )
    category_level_5 = fields.Char(string="Category Level 5", required=False, )

    variant_1_attribute = fields.Char(string="Variant 1 Attribute", required=False, )
    variant_1_attribute_value = fields.Char(string="Variant 1 Attribute Value", required=False, )

    variant_2_attribute = fields.Char(string="Variant 2 Attribute", required=False, )
    variant_2_attribute_value = fields.Char(string="Variant 2 Attribute Value", required=False, )

    variant_3_attribute = fields.Char(string="Variant 3 Attribute", required=False, )
    variant_3_attribute_value = fields.Char(string="Variant 3 Attribute Value", required=False, )

    variant_4_attribute = fields.Char(string="Variant 4 Attribute", required=False, )
    variant_4_attribute_value = fields.Char(string="Variant 4 Attribute Value", required=False, )

    variant_5_attribute = fields.Char(string="Variant 5 Attribute", required=False, )
    variant_5_attribute_value = fields.Char(string="Variant 5 Attribute Value", required=False, )

    variant_6_attribute = fields.Char(string="Variant 6 Attribute", required=False, )
    variant_6_attribute_value = fields.Char(string="Variant 6 Attribute Value", required=False, )

    variant_7_attribute = fields.Char(string="Variant 7 Attribute", required=False, )
    variant_7_attribute_value = fields.Char(string="Variant 7 Attribute Value", required=False, )

    variant_8_attribute = fields.Char(string="Variant 8 Attribute", required=False, )
    variant_8_attribute_value = fields.Char(string="Variant 8 Attribute Value", required=False, )

    variant_9_attribute = fields.Char(string="Variant 9 Attribute", required=False, )
    variant_9_attribute_value = fields.Char(string="Variant 9 Attribute Value", required=False, )

    variant_10_attribute = fields.Char(string="Variant 10 Attribute", required=False, )
    variant_10_attribute_value = fields.Char(string="Variant 10 Attribute Value", required=False, )

    desc_field_1 = fields.Char(string="Description Field 1", required=False, )
    desc_field_2 = fields.Char(string="Description Field 2", required=False, )
    desc_field_3 = fields.Char(string="Description Field 3", required=False, )
    desc_field_4 = fields.Char(string="Description Field 4", required=False, )
    desc_field_5 = fields.Char(string="Description Field 5", required=False, )
    desc_field_6 = fields.Char(string="Description Field 6", required=False, )
    desc_field_7 = fields.Char(string="Description Field 7", required=False, )
    desc_field_8 = fields.Char(string="Description Field 8", required=False, )
    desc_field_9 = fields.Char(string="Description Field 9", required=False, )
    desc_field_10 = fields.Char(string="Description Field 10", required=False, )
    is_created = fields.Boolean('Created', default=True)
    volume = fields.Float('Volume')
    sale_delay = fields.Float('Customer Lead Time')
    category_path = fields.Char('Category Path')
    vendor_name = fields.Char("Vendor Name")
    min_qty = fields.Float("Min Qty")
    delay = fields.Float("Delay1")
    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)', "An internal reference can only be assigned to one product !"),
    ]
