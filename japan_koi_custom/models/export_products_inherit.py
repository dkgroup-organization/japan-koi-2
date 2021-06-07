# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import api, fields, models, _
from odoo.addons.prestashop_odoo_bridge.models.prestapi import PrestaShopWebService,PrestaShopWebServiceDict,PrestaShopWebServiceError,PrestaShopAuthenticationError
from odoo.exceptions import  UserError,RedirectWarning, ValidationError ,Warning
from odoo.addons.odoo_multi_channel_sale.tools import extract_list as EL
from odoo.addons.odoo_multi_channel_sale.tools import ensure_string as ES
from odoo.addons.odoo_multi_channel_sale.tools import JoinList as JL
from odoo.addons.odoo_multi_channel_sale.tools import MapId
import logging
_logger = logging.getLogger(__name__)

class ExportProductsInherit(models.TransientModel):
    _inherit = 'export.templates'
    
# override funtion export update template product     
    def prestashop_export_now(self, record):
        res = [False, ""]
        if record.type == "service" :
            return res
        if record.attribute_line_ids and len(record.product_variant_ids.filtered(lambda r: r.display_vente))==0:
            return res           
        if not record.attribute_line_ids and not record.product_variant_id.display_vente :
            return res
        channel_id = self._context.get('channel_id')
        variant_list = []
        prestashop = self._context.get('prestashop')
        try:
            product_bs = prestashop.get('products', options={'schema': 'blank'})
            response = self.prestashop_export_template(
                prestashop, channel_id, product_bs, record)
            if not response[0]:
                return res
            ps_template_id = response[1]
            remote_object = {}
            if record.attribute_line_ids:
                default_variant = record.product_variant_id.id
                for variant_id in record.product_variant_ids.filtered(lambda r: r.display_vente):
                    default_attr = "0"
                    if variant_id.id == default_variant:
                        default_attr = "1"
                    response = self.create_combination(
                        prestashop, channel_id, ps_template_id, variant_id,default_attr)
                    if response[0]:
                        variant_list.append(response[1])
                if variant_list:
                    remote_object["id"] = ps_template_id
                    remote_object["variants"] = [{"id": variant_id} for variant_id in variant_list]
                    res = [True, remote_object]
            elif record.product_variant_id.display_vente:
                product_data = prestashop.get("products",ps_template_id)
                stock_id = product_data.get("product").get(
                    "associations",{}).get("stock_availables",{}).get("stock_available",{}).get("id")
                self.create_normal_product(
                    prestashop, channel_id,record.product_variant_id , ps_template_id,stock_id)
                remote_object["id"] = ps_template_id
                remote_object["variants"] = [{"id":"No Variants"}]
                res = [True, remote_object]
        except Exception as e:
            _logger.info("Error in creating products : %r",str(e))
        return res
    
    
    
    def prestashop_update_template(self, prestashop, channel_id, product_bs, template_record, remote_id):
        cost = template_record.standard_price
        default_code = template_record.default_code or ''
        erp_category_id = template_record.categ_id
        presta_default_categ_id = self._get_store_categ_id(
            prestashop, erp_category_id)
        ps_extra_categ = []
        extra_categories_set = set()
        extra_categories = template_record.channel_category_ids
        extra_categories = extra_categories.filtered(lambda x: x.instance_id.id == channel_id.id)
        if extra_categories:
            for extra_category in extra_categories:
                for categ in extra_category.extra_category_ids:
                    cat_id = self._get_store_categ_id(prestashop, categ)
                    if cat_id not in extra_categories_set:
                        extra_categories_set.add(cat_id)
                        ps_extra_categ.append({'id': str(cat_id)})
        product_bs['product'].update({
            'price': str(round(template_record.with_context(pricelist=channel_id.pricelist_name.id).price, 2)),
            'active': '1',
            'weight': str(template_record.weight) or '',
            'redirect_type': '404',
            'minimal_quantity': '1',
            'available_for_order': '1',
            'show_price': '1',
            'depth': str(template_record.wk_length) or '',
            'width': str(template_record.width) or '',
            'height': str(template_record.height) or '',
            'state': '1',
            'ean13': template_record.barcode or '',
            'position': template_record.sequence or 0,
            'reference': default_code or '',
            'out_of_stock': '2',
            'condition': 'new',
            'special_delivery':'1' if template_record.special_delivery_customer else '0',
            'variety': template_record.variete if template_record.variete else '',
            'age': template_record.age if template_record.age else '',
            'breeder': template_record.eleveur if template_record.eleveur else '',
            'quality':template_record.qualite if template_record.qualite else '',
            'size':template_record.taille if template_record.taille else '',
            'video_link': template_record.lien_video if template_record.lien_video else '',
            'id_category_default': str(presta_default_categ_id)
        })
        #Trier la liste des produits par numéro séquence 
        if cost:
            product_bs['product']['wholesale_price'] = str(round(cost, 3))
        if type(product_bs['product']['name']['language']) == list:
            for i in range(len(product_bs['product']['name']['language'])):
                product_bs['product']['name']['language'][i]['value'] = template_record.name
                product_bs['product']['link_rewrite']['language'][i]['value'] = channel_id._get_link_rewrite(
                    '', template_record.name)
                product_bs['product']['description']['language'][i]['value'] = template_record.description_sale or ""
                product_bs['product']['description_short']['language'][i]['value'] = template_record.description or ""
        else:
            product_bs['product']['name']['language']['value'] = template_record.name
            product_bs['product']['link_rewrite']['language']['value'] = channel_id._get_link_rewrite(
                '', template_record.name)
            product_bs['product']['description']['language']['value'] = template_record.description or ""
            product_bs['product']['description_short']['language']['value'] = template_record.description_sale or ""
        if 'category' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['category']['id'] = str(
                presta_default_categ_id)
        if 'categories' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['categories']['id'] = str(
                presta_default_categ_id)
        product_bs['product']['associations'].pop(
            'combinations', None)
        product_bs['product']['associations'].pop('images', None)
        product_bs['product'].pop('position_in_category', None)
        product_bs['product'].pop('manufacturer_name', None)
        product_bs['product'].pop('quantity', None)
        if ps_extra_categ:
            if 'category' in product_bs['product']['associations']['categories']:
                product_bs['product']['associations']['categories']['category'] = ps_extra_categ
            if 'categories' in product_bs['product']['associations']['categories']:
                product_bs['product']['associations']['categories']['categories'] = ps_extra_categ
        try:
            prestashop.edit('products', remote_id, product_bs)
        except Exception as e:
            _logger.info("Error in updating Product Template : %r", str(e))
            if channel_id.debug == "enable":
                raise UserError( f'Error in updating Product Template : {e}')
            return [False, ""]
        return [True, remote_id]

    def prestashop_export_template(self, prestashop, channel_id, product_bs, template_record):
        #raise ValidationError(product_bs)
        cost = template_record.standard_price
        default_code = template_record.default_code or ''
        erp_category_id = template_record.categ_id
        presta_default_categ_id = self._get_store_categ_id(
            prestashop, erp_category_id)
        ps_extra_categ = []
        extra_categories_set = set()
        extra_categories = template_record.channel_category_ids
        extra_categories = extra_categories.filtered(lambda x: x.instance_id.id == channel_id.id)
        if extra_categories:
            for extra_category in extra_categories:
                for categ in extra_category.extra_category_ids:
                    cat_id = self._get_store_categ_id(prestashop, categ)
                    if cat_id not in extra_categories_set:
                        extra_categories_set.add(cat_id)
                        ps_extra_categ.append({'id': str(cat_id)})
        features = {'feature':'Livraison speciale','value':'Non'}

        product_bs['product'].update({
            'price': str(round(template_record.with_context(pricelist=channel_id.pricelist_name.id).price, 2)),
            'active': '1',
            'weight': str(template_record.weight) or '',
            'redirect_type': '404',
            'minimal_quantity': '1',
            'available_for_order': '1',
            'show_price': '1',
            'depth': str(template_record.wk_length) or '',
            'width': str(template_record.width) or '',
            'height': str(template_record.height) or '',
            'state': '1',
            'ean13': template_record.barcode or '',
            'position':template_record.sequence or 0,
            'reference': default_code or '',
            'out_of_stock': '2',
            'condition': 'new',
            'special_delivery':'1' if template_record.special_delivery_customer else '0',
            'variety': template_record.variete if template_record.variete else '',
            'age': template_record.age if template_record.age else '',
            'breeder': template_record.eleveur if template_record.eleveur else '',
            'quality':template_record.qualite if template_record.qualite else '',
            'size':template_record.taille if template_record.taille else '',
            'video_link': template_record.lien_video if template_record.lien_video else '',
            'id_category_default': str(presta_default_categ_id)
        })
        if cost:
            product_bs['product']['wholesale_price'] = str(round(cost, 3))
        if type(product_bs['product']['name']['language']) == list:
            for i in range(len(product_bs['product']['name']['language'])):
                product_bs['product']['name']['language'][i]['value'] = template_record.name
                product_bs['product']['link_rewrite']['language'][i]['value'] = channel_id._get_link_rewrite(
                    '', template_record.name)
                product_bs['product']['description']['language'][i]['value'] = template_record.description or ""
                product_bs['product']['description_short']['language'][i]['value'] = template_record.description_sale or ""
        else:
            product_bs['product']['name']['language']['value'] = template_record.name
            product_bs['product']['link_rewrite']['language']['value'] = channel_id._get_link_rewrite(
                '', template_record.name)
            product_bs['product']['description']['language']['value'] = template_record.description or ""
            product_bs['product']['description_short']['language']['value'] = template_record.description_sale or ""
        if 'category' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['category']['id'] = str(
                presta_default_categ_id)
        if 'categories' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['categories']['id'] = str(
                presta_default_categ_id)
        product_bs['product']['associations'].pop(
            'combinations', None)
        product_bs['product']['associations'].pop('images', None)
        product_bs['product'].pop('position_in_category', None)
        product_bs['product'].pop('manufacturer_name', None)

        if ps_extra_categ:
            if 'category' in product_bs['product']['associations']['categories']:
                product_bs['product']['associations']['categories']['category'] = ps_extra_categ
            if 'categories' in product_bs['product']['associations']['categories']:
                product_bs['product']['associations']['categories']['categories'] = ps_extra_categ
        try:
            returnid = prestashop.add('products', product_bs)
        except Exception as e:
            _logger.info("Error in creating Product Template : %r", str(e))
            if channel_id.debug in ["enable"]:
                raise UserError(f"Error in creating Product Template : {e}")
            return [False, ""]
        return [True, returnid]

    
    
    
