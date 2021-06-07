# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Simple Product Brand',
    'version': '14.0.0.0.1',
    'category': 'Product Management',
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'LGPL-3',
    'website': 'http://www.ictstudio.eu',
    'summary': """Simple Product Brand """,
    'depends': [
        'base',
        'sale',
        'purchase',
        'account',

    ],
    'data': [
        'views/product_product.xml',
        'views/product_template.xml',
        'views/simple_product_brand.xml',
        'security/ir.model.access.csv',
        #'report/account_invoice_report.xml',
        'report/purchase_report.xml',
        'report/sale_report.xml'
    ],
    'installable': True,
}
