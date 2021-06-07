# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from PIL import Image
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import Warning, UserError, AccessError
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.tools import sql


import logging
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class import_product_var_wizard(models.TransientModel):
    _name = "import.product.var.wizard"
    _description = "Wizard Import Product Variant Wizard"

    def import_product_var_apply(self):  # Through wizard

        # - If excel not yet imported display warning : please import excel file before
        variant_ids = self.env['dkg.import.product.variant.template'].search([
        ])
        if variant_ids:
            catge_obj = self.env['product.category']
            attribute_obj = self.env['product.attribute']
            attribute_value_obj = self.env['product.attribute.value']
            product_tmpl_obj = self.env['product.template']
            category_ids = {}
            is_import = False
            for i in variant_ids:
                if not i.is_created:
                    continue
                product_tmpl_obj_all = self.env['dkg.import.product.variant.template'].search([('name', '=', i.name)])
                varint_ids = []
                varint_value_ids = {}
                count = 0
                for rec in product_tmpl_obj_all:
                    if not rec.is_created:
                        continue
                    count += 1
                    catege_id = 0
                    category_ids[rec.id] = 0
                    if rec.category_level_0:
                        category_level_0 = catge_obj.search(
                            [('name', '=', rec.category_level_0.strip().capitalize())])
                        if not category_level_0:
                            category_level_0 = catge_obj.create({
                                'name': rec.category_level_0.strip().capitalize(),
                                'parent_id': False
                            })
                        
                        catege_id = category_level_0
                        category_ids[rec.id] = catege_id.id
                        if rec.category_level_1:
                            category_level_1 = catge_obj.search([('name', '=', rec.category_level_1.strip(
                            ).capitalize()), ('parent_id', '=', category_level_0.id)])
                            if not category_level_1:
                                category_level_1 = catge_obj.create({
                                    'name': rec.category_level_1.strip().capitalize(),
                                    'parent_id': category_level_0.id
                                })
                            catege_id = category_level_1
                            category_ids[rec.id] = catege_id.id
                            if rec.category_level_2:
                                category_level_2 = catge_obj.search([('name', '=', rec.category_level_2.strip(
                                ).capitalize()), ('parent_id', '=', category_level_1.id)])
                                if not category_level_2:
                                    category_level_2 = catge_obj.create({
                                        'name': rec.category_level_2.strip().capitalize(),
                                        'parent_id': category_level_1.id
                                    })
                                catege_id = category_level_2
                                category_ids[rec.id] = catege_id.id
                                if rec.category_level_3:
                                    category_level_3 = catge_obj.search([('name', '=', rec.category_level_3.strip(
                                    ).capitalize()), ('parent_id', '=', category_level_2.id)])
                                    if not category_level_3:
                                        category_level_3 = catge_obj.create({
                                            'name': rec.category_level_3.strip().capitalize(),
                                            'parent_id': category_level_2.id
                                        })
                                    catege_id = category_level_3
                                    category_ids[rec.id] = catege_id.id
                                    if rec.category_level_4:
                                        category_level_4 = catge_obj.search([('name', '=', rec.category_level_4.strip(
                                        ).capitalize()), ('parent_id', '=', category_level_3.id)])
                                        if not category_level_4:
                                            category_level_4 = catge_obj.create({
                                                'name': rec.category_level_4.strip().capitalize(),
                                                'parent_id': category_level_3.id
                                            })
                                        catege_id = category_level_4
                                        category_ids[rec.id] = catege_id.id
                                        if rec.category_level_5:
                                            category_level_5 = catge_obj.search([('name', '=', rec.category_level_5.strip(
                                            ).capitalize()), ('parent_id', '=', category_level_4.id)])
                                            if not category_level_5:
                                                category_level_5 = catge_obj.create({
                                                    'name': rec.category_level_5.strip().capitalize(),
                                                    'parent_id': category_level_4.id
                                                })
                                            catege_id = category_level_5
                                            category_ids[rec.id] = catege_id.id                    
                    if rec.variant_1_attribute and rec.variant_1_attribute_value :
                        attribute_id = attribute_obj.search([('name', '=', rec.variant_1_attribute.strip().capitalize())])
                        if not attribute_id:
                            attribute_id = attribute_obj.create({
                                'name' : rec.variant_1_attribute.strip().capitalize()
                            })
                        attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_1_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                        if not attribute_value_id:
                            attribute_value_id = attribute_value_obj.create({
                                'name' : rec.variant_1_attribute_value.strip().capitalize(),
                                'attribute_id': attribute_id.id
                            })
                        if attribute_id.id not in varint_ids:
                            varint_ids.append(attribute_id.id)
                        if varint_value_ids.get(attribute_id.id):
                            if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                        else:
                            varint_value_ids[attribute_id.id] = [attribute_value_id.id]
                    if rec.variant_2_attribute and rec.variant_2_attribute_value:
                        attribute_id = attribute_obj.search([('name', '=', rec.variant_2_attribute.strip().capitalize())])
                        if not attribute_id:
                            attribute_id = attribute_obj.create({
                                'name' : rec.variant_2_attribute.strip().capitalize()
                            })
                        attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_2_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                        if not attribute_value_id:
                            attribute_value_id = attribute_value_obj.create({
                                'name' : rec.variant_2_attribute_value.strip().capitalize(),
                                'attribute_id': attribute_id.id
                            })
                        if attribute_id.id not in varint_ids:
                            varint_ids.append(attribute_id.id)
                        if varint_value_ids.get(attribute_id.id):
                            if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                        else:
                            varint_value_ids[attribute_id.id] = [attribute_value_id.id]
                    if rec.variant_3_attribute and rec.variant_3_attribute_value:
                        attribute_id = attribute_obj.search([('name', '=', rec.variant_3_attribute.strip().capitalize())])
                        if not attribute_id:
                            attribute_id = attribute_obj.create({
                                'name' : rec.variant_3_attribute.strip().capitalize()
                            })
                        attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_3_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                        if not attribute_value_id:
                            attribute_value_id = attribute_value_obj.create({
                                'name' : rec.variant_3_attribute_value.strip().capitalize(),
                                'attribute_id': attribute_id.id
                            })
                        if attribute_id.id not in varint_ids:
                            varint_ids.append(attribute_id.id)
                        if varint_value_ids.get(attribute_id.id):
                            if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                        else:
                            varint_value_ids[attribute_id.id] = [attribute_value_id.id]

                    if rec.variant_4_attribute and rec.variant_4_attribute_value:
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_4_attribute.strip().capitalize())])
                            if not attribute_id:
                                attribute_id = attribute_obj.create({
                                    'name' : rec.variant_4_attribute.strip().capitalize()
                                })
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_4_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            if not attribute_value_id:
                                attribute_value_id = attribute_value_obj.create({
                                    'name' : rec.variant_4_attribute_value.strip().capitalize(),
                                    'attribute_id': attribute_id.id
                                })
                            if attribute_id.id not in varint_ids:
                                varint_ids.append(attribute_id.id)
                            if varint_value_ids.get(attribute_id.id):
                                if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                    varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                            else:
                                varint_value_ids[attribute_id.id] = [attribute_value_id.id]

                    if rec.variant_5_attribute and rec.variant_5_attribute_value:
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_5_attribute.strip().capitalize())])
                            if not attribute_id:
                                attribute_id = attribute_obj.create({
                                    'name' : rec.variant_5_attribute.strip().capitalize()
                                })
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_5_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            if not attribute_value_id:
                                attribute_value_id = attribute_value_obj.create({
                                    'name' : rec.variant_5_attribute_value.strip().capitalize(),
                                    'attribute_id': attribute_id.id
                                })
                            if attribute_id.id not in varint_ids:
                                varint_ids.append(attribute_id.id)
                            if varint_value_ids.get(attribute_id.id):
                                if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                    varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                            else:
                                varint_value_ids[attribute_id.id] = [attribute_value_id.id]

                    if rec.variant_6_attribute and rec.variant_6_attribute_value:
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_6_attribute.strip().capitalize())])
                            if not attribute_id:
                                attribute_id = attribute_obj.create({
                                    'name' : rec.variant_6_attribute.strip().capitalize()
                                })
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_6_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            if not attribute_value_id:
                                attribute_value_id = attribute_value_obj.create({
                                    'name' : rec.variant_6_attribute_value.strip().capitalize(),
                                    'attribute_id': attribute_id.id
                                })
                            if attribute_id.id not in varint_ids:
                                varint_ids.append(attribute_id.id)
                            if varint_value_ids.get(attribute_id.id):
                                if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                    varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                            else:
                                varint_value_ids[attribute_id.id] = [attribute_value_id.id]

                    if rec.variant_7_attribute and rec.variant_7_attribute_value:
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_7_attribute.strip().capitalize())])
                            if not attribute_id:
                                attribute_id = attribute_obj.create({
                                    'name' : rec.variant_7_attribute.strip().capitalize()
                                })
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_7_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            if not attribute_value_id:
                                attribute_value_id = attribute_value_obj.create({
                                    'name' : rec.variant_7_attribute_value.strip().capitalize(),
                                    'attribute_id': attribute_id.id
                                })
                            if attribute_id.id not in varint_ids:
                                varint_ids.append(attribute_id.id)
                            if varint_value_ids.get(attribute_id.id):
                                if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                    varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                            else:
                                varint_value_ids[attribute_id.id] = [attribute_value_id.id]

                    if rec.variant_8_attribute and rec.variant_8_attribute_value:
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_8_attribute.strip().capitalize())])
                            if not attribute_id:
                                attribute_id = attribute_obj.create({
                                    'name' : rec.variant_8_attribute.strip().capitalize()
                                })
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_8_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            if not attribute_value_id:
                                attribute_value_id = attribute_value_obj.create({
                                    'name' : rec.variant_8_attribute_value.strip().capitalize(),
                                    'attribute_id': attribute_id.id
                                })
                            if attribute_id.id not in varint_ids:
                                varint_ids.append(attribute_id.id)
                            if varint_value_ids.get(attribute_id.id):
                                if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                    varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                            else:
                                varint_value_ids[attribute_id.id] = [attribute_value_id.id]
                    if rec.variant_9_attribute and rec.variant_9_attribute_value:
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_9_attribute.strip().capitalize())])
                            if not attribute_id:
                                attribute_id = attribute_obj.create({
                                    'name' : rec.variant_9_attribute.strip().capitalize()
                                })
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_9_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            if not attribute_value_id:
                                attribute_value_id = attribute_value_obj.create({
                                    'name' : rec.variant_9_attribute_value.strip().capitalize(),
                                    'attribute_id': attribute_id.id
                                })
                            if attribute_id.id not in varint_ids:
                                varint_ids.append(attribute_id.id)
                            if varint_value_ids.get(attribute_id.id):
                                if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                    varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                            else:
                                varint_value_ids[attribute_id.id] = [attribute_value_id.id]
                    
                    if rec.variant_10_attribute and rec.variant_10_attribute_value:
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_10_attribute.strip().capitalize())])
                            if not attribute_id:
                                attribute_id = attribute_obj.create({
                                    'name' : rec.variant_10_attribute.strip().capitalize()
                                })
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_10_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            if not attribute_value_id:
                                attribute_value_id = attribute_value_obj.create({
                                    'name' : rec.variant_10_attribute_value.strip().capitalize(),
                                    'attribute_id': attribute_id.id
                                })
                            if attribute_id.id not in varint_ids:
                                varint_ids.append(attribute_id.id)
                            if varint_value_ids.get(attribute_id.id):
                                if attribute_value_id.id not in varint_value_ids.get(attribute_id.id):
                                    varint_value_ids.get(attribute_id.id).append(attribute_value_id.id)
                            else:
                                varint_value_ids[attribute_id.id] = [attribute_value_id.id]
                vals = {
                    'name' : i.name.strip().capitalize(),
                    'type' : i.type,
                    'sale_ok': i.sale_ok,
                    'purchase_ok': i.purchase_ok,
                    'taxes_id': [(6, 0, i.taxes_id.ids)],
                    'supplier_taxes_id': [(6, 0, i.supplier_taxes_id.ids)],
                    'invoice_policy': i.invoice_policy,
                    'uom_id': i.uom_id.id,
                    'uom_po_id': i.uom_po_id.id,
                    'description_sale': i.description_sale,
                    'categ_id' : category_ids[i.id] or 1,
                }
                atr_li = []
                for atr in varint_ids:
                   
                    atr_li.append(tuple((0, 0, {
                        'attribute_id' : atr,
                        'value_ids': [(6, 0,  varint_value_ids.get(atr))]
                    })))
                vals.update({
                    'attribute_line_ids' : atr_li
                })
                if i.type:
                    product_varint_obj = self.env['product.template.attribute.value']
                    product_id = product_tmpl_obj.create(vals)
                    product_obj = self.env['product.product'] 
                    var_ids = product_obj.search([
                        ('product_tmpl_id', '=', product_id.id)
                    ])
                    for rec in product_tmpl_obj_all:
                        attribute_value_ids = []
                        product_ids = []
                        if rec.variant_1_attribute and rec.variant_1_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_1_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_1_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_2_attribute and rec.variant_2_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_2_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_2_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_3_attribute and rec.variant_3_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_3_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_3_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                        if rec.variant_4_attribute and rec.variant_4_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_4_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_4_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_5_attribute and rec.variant_5_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_5_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_5_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_6_attribute and rec.variant_6_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_6_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_6_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_7_attribute and rec.variant_7_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_7_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_7_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_8_attribute and rec.variant_8_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_8_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_8_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_9_attribute and rec.variant_9_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_9_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_9_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                            
                        if rec.variant_10_attribute and rec.variant_10_attribute_value :
                            attribute_id = attribute_obj.search([('name', '=', rec.variant_10_attribute.strip().capitalize())])
                            attribute_value_id = attribute_value_obj.search([('name', '=', rec.variant_10_attribute_value.strip().capitalize()), ('attribute_id', '=', attribute_id.id)])
                            product_varint_id = product_varint_obj.search([('product_tmpl_id', '=', product_id.id), ('product_attribute_value_id', '=', attribute_value_id.id)])
                            attribute_value_ids.append(product_varint_id.id)
                            domain = []
                            if product_ids:
                                domain = [('id', 'in', product_ids)]
                            var_ids = product_obj.search([
                                ('product_tmpl_id', '=', product_id.id),
                                ('product_template_attribute_value_ids', 'in', [product_varint_id.id]),
                            ] + domain)
                            if var_ids:
                                product_ids = var_ids.ids
                        for product in var_ids:
                            is_import = True
                            barcode_product = product_obj.search([(
                                'barcode', '=', rec.barcode.upper()
                            )])
                            barcode_data = rec.barcode
                            if barcode_product and barcode_data:
                                barcode_data += rec.barcode + 'D' 
                                barcode_product = product_obj.search([(
                                    'barcode', 'ilike', barcode_data.upper()
                                )]) 
                                if barcode_product:
                                    bar = []
                                    for br in barcode_product.mapped('barcode'):
                                        bar.append(int(br.split('D')[1]))
                                    max_bar = max(bar)
                                    barcode_data += str(max_bar + 1)
                                else:
                                    barcode_data += '1'
                            vals ={
                                'description_sale': rec.description_sale,
                                'default_code': rec.default_code.upper(),
                                'barcode': barcode_data and barcode_data.upper() or False,
                                'weight': rec.weight,
                                'standard_price': rec.standard_price,
                                'fix_price': rec.fix_price,
                            }
                            product.write(vals)
                        rec.is_created = False
            product_ids = self.env['product.product'].search([('name', '=', i.name.strip().capitalize()), ('default_code', '=', False)])
            product_ids.write({
                'active' : False
            })

            if not is_import:
                raise Warning("No data Imported either data was already imported or something missing!")    
        else:
            raise Warning(
                "No data exist please fill the template, import it, then launch this wizard")

######### - Fields Case Treatment Guide ##################################################################
            # - Uppercase and strip : External ID, Internal Reference, Barcode, Variant Attribute, Variant Attribute Value
            # - Propercase and strip for : Name, Categories All Levels (0-5), Sales Description
# - Duplicata Treatment Guide
            # - Detect duplicates on Internal Reference, Barcode >> Add "- D + Number of duplication"
            #   for duplicated values (Do Not Delete Any Record Given By Customer) ex: 890 / 890-D1

##########################################################################################################

######### - Algorithme steps #############################################################################
            # - Product category unify names use strip and PROPER then from output remove duplicated and create
            #   categories and them parents
            #   Propercase and strip for : Name, Categories All Levels (0-5), Sales Description

            # - Loop and create product template then them variants (better template followed by it's variants)
            #   If error display warning with product internal reference
            # - Product category : Concatenate (categ level 0 / categ level 1 / categ level 2 ... / categ level 5)
            # - For fixed price check if OCA module price_fix is installed, when importing fix_price column
            ######### - Fields Case Treatment Guide ##################################################################
            # - Uppercase and strip : External ID, Internal Reference, Barcode, Variant Attribute, Variant Attribute Value
            # - Propercase and strip for : Name, Categories All Levels (0-5), Sales Description
            # - Duplicata Treatment Guide
            # - Detect duplicates on Internal Reference, Barcode >> Add "- D + Number of duplication"
            #   for duplicated values (Do Not Delete Any Record Given By Customer) ex: 890 / 890-D1
