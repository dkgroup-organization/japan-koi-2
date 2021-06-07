# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'All In One Cancel Sales,Purchases and Delivery/Incoming Shipments',
    'version' : '1.0',
    'author':'Craftsync Technologies',
    'category': 'Sales',
    'maintainer': 'Craftsync Technologies',
    'summary': """Enable Auto cancel like Sales Purchase and invoice, Inventory . This module it will allow you cancel sale,purchase,accounting,Inventory even if it already done. """,

    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'depends' : ['purchase_stock',
    		#'account_cancel',
    		'sale_management',
    		'sale_stock'],
    'data': [

        'views/res_config_settings_views.xml',
        'views/view_purchase_order.xml',
        'views/stock_warehouse.xml',
        'views/view_sale_order.xml',
        'views/stock_picking.xml',
        'wizard/view_cancel_delivery_wizard.xml',
        'security/ir.model.access.csv'

    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 34.99,
    'currency': 'EUR',

    'images': ['static/description/main_screen.png'],

}
