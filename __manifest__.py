# -*- coding: utf-8 -*-
{
    'name': 'SIE - Módulo Propio Siempre Unidos',
    'version': '16.0.1.0.0',
    'category': 'Custom',
    'summary': 'Módulo propio para la gestión de información del sistema SIE.',
    'description': """
SIE - Módulo Propio Siempre Unidos
====================================
Módulo personalizado para la gestión de registros y miembros del sistema SIE.

Funcionalidades:
- Gestión de miembros
- Seguimiento de actividades
- Reportes personalizados
    """,
    'author': 'Siempre Unidos',
    'website': 'https://github.com/Pedmatgar/sie-modulo-propio-siempre-unidos',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sie_sequence.xml',
        'views/sie_member_views.xml',
        'views/sie_menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
