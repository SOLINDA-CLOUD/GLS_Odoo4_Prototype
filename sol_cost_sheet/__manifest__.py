# -*- coding: utf-8 -*-
{
    'name': "sol_cost_sheet",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','sale_crm','sale_project','purchase_request'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/master_item.xml',
        'views/crm_views.xml',
        'views/sale_order_views.xml',
        'views/cost_sheet_views.xml',
        'views/costsheet_component_views.xml',
        'wizard/cost_sheet_component.xml',
        'views/project_views.xml',
        'views/rap_views.xml',
        'views/menuitem.xml',
        'views/sequence_data.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3'
}
