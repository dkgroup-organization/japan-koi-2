# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Import Invoice Lines from CSV File | Import Invoice Lines from Excel file",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "license": "OPL-1",
    "summary": "Import Bill Lines From CSV App, Import lines From Excel Module , Import Invoice Lines From CSV, Import Invoice Lines From Excel, import Bill Lines From XLS XLSX Odoo",
    "description": """
    This module is useful to import invoice/bill lines with from CSV/Excel file. You can import custom fields from CSV or Excel.

 Import Invoice / Bill Lines From CSV Odoo, Import Invoice / Bill Lines Of Materials From excel Odoo
 Import Bill Lines From CSV Module, Import Bill Lines From Excel, Import Bill Lines From XLS XLSX, Import Invoice Lines From CSV, Import Invoice Lines From Excel Odoo.
 Import Bill Lines From CSV App, Import lines From Excel Module , Import Invoice Lines From CSV, Import Invoice Lines From Excel, import Bill Lines From XLS XLSX Odoo . 
Importar facturas / líneas de factura de CSV Odoo, Importar facturas / líneas de factura de materiales de Excel Odoo
 Importar líneas de factura desde el módulo CSV, Importar líneas de factura desde Excel, Importar líneas de factura desde XLS XLSX, Importar líneas de factura desde CSV, Importar líneas de factura desde Excel Odoo.
 Importar líneas de factura desde la aplicación CSV, Importar líneas desde el módulo Excel, Importar líneas de factura desde CSV, Importar líneas de factura desde Excel, importar líneas de factura desde XLS XLSX Odoo.

                    """,
    "version": "14.0.1",
    "depends": [
        "account",
        "sh_message",
    ],
    "application": True,
    "data": [
        'security/import_ail_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_ail_wizard.xml',
        'views/account_view.xml',
    ],
    'external_dependencies': {
        'python': ['xlrd'],
    },
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/ymJ-xW18hD8",
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
