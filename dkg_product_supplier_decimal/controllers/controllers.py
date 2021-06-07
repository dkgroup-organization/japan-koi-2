# -*- coding: utf-8 -*-
# from odoo import http


# class ProductSupplierDecimal(http.Controller):
#     @http.route('/product_supplier_decimal/product_supplier_decimal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_supplier_decimal/product_supplier_decimal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_supplier_decimal.listing', {
#             'root': '/product_supplier_decimal/product_supplier_decimal',
#             'objects': http.request.env['product_supplier_decimal.product_supplier_decimal'].search([]),
#         })

#     @http.route('/product_supplier_decimal/product_supplier_decimal/objects/<model("product_supplier_decimal.product_supplier_decimal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_supplier_decimal.object', {
#             'object': obj
#         })
