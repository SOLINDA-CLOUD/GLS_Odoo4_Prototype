# -*- coding: utf-8 -*-
{
    'name': "Cost Sheet",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Siwi Wiyono Raharjo",
    'website': "https://www.linkedin.com/in/siwiyono",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','sale_project','sale_crm','purchase_requisition','purchase','mrp','report_py3o'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_views.xml',
        'views/mrp_views.xml',
        'views/product_template_views.xml',
        'views/rab_template_views.xml',
        'views/cost_sheet_views.xml',
        'views/rap_views.xml',
        'views/purchase_requisition_views.xml',
        'views/project_views.xml',
        'views/sale_order_views.xml',
        'views/approval_views.xml',
        'views/sequence_data.xml',
        'views/purchase_order_views.xml',
        'report/action_report.xml',
        'report/rab_report_template.xml',
        'report/report_rfq.xml',
        'views/menuitem_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    'license': 'LGPL-3'
}
