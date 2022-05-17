# -*- coding: utf-8 -*-
{
    'name': "GLS Reporting",

    'summary': """
        Reporting Module
        """,

    'description': """
        Reporting Module for GLS
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'report/action_report.xml',
        'report/report_quotation_boo.xml',
        'report/report_quotation_oms.xml',
        'report/report_quotation_trading.xml',
        'report/report_quotation_turnkey.xml',
    ],
    'license': 'LGPL-3'
    
}
