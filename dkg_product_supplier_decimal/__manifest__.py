# -*- coding: utf-8 -*-
{
    'name': "product_supplier_decimal",

    'summary': """
            Add decimal precision on supplier info""",

    'description': """
        Add decimal precision on supplier info
    """,

    'author': "DKG",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'product',
                'sale',
                'purchase',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
