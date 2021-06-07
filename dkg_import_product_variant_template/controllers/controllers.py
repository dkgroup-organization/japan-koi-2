# -*- coding: utf-8 -*-
# from odoo import http


# class ImportProductVariantTemplate(http.Controller):
#     @http.route('/import_product_variant_template/import_product_variant_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/import_product_variant_template/import_product_variant_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('import_product_variant_template.listing', {
#             'root': '/import_product_variant_template/import_product_variant_template',
#             'objects': http.request.env['import_product_variant_template.import_product_variant_template'].search([]),
#         })

#     @http.route('/import_product_variant_template/import_product_variant_template/objects/<model("import_product_variant_template.import_product_variant_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('import_product_variant_template.object', {
#             'object': obj
#         })
