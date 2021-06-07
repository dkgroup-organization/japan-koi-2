# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Simple Product Brand Pricelist',
    'version': '13.0.0.0.1',
    'category': 'Product Management',
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'LGPL-3',
    'website': 'http://www.ictstudio.eu',
    'summary': """Advanced Pricelist calculation based on brands""",
    'depends': [
        "simple_product_brand"
    ],
    'data': [
        'views/product_pricelist_item.xml',
    ],
    'installable': True,
}
