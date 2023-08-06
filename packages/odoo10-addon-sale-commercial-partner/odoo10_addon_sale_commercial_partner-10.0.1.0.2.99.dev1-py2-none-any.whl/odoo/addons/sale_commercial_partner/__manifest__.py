# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Commercial Partner',
    'version': '10.0.1.0.2',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': "Add stored related field 'Commercial Entity' on sale orders",
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/sale-workflow',
    'depends': ['sale'],
    'data': [
        'views/sale.xml',
    ],
    'installable': True,
}
