# -*- coding: utf-8 -*-
# from odoo import http


# class JapanKoiCustom(http.Controller):
#     @http.route('/japan_koi_custom/japan_koi_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/japan_koi_custom/japan_koi_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('japan_koi_custom.listing', {
#             'root': '/japan_koi_custom/japan_koi_custom',
#             'objects': http.request.env['japan_koi_custom.japan_koi_custom'].search([]),
#         })

#     @http.route('/japan_koi_custom/japan_koi_custom/objects/<model("japan_koi_custom.japan_koi_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('japan_koi_custom.object', {
#             'object': obj
#         })
