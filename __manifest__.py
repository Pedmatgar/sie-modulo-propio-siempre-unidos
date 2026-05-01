{
    'name': "Subcontrataciones",
    'version': '1.0',
    'depends': ['base', 'contacts'],
    'author': "SIEmpre Unidos",
    'category': 'Human Resources',
    'description': """
        Módulo de gestión de subcontratos con personal externo.
        Permite registrar, consultar y eliminar automáticamente los contratos
        activos de empresas (De mantenimiento, de reparación, etc.) o de 
        empleados particulares asignados a las comunidades gestionadas por la empresa.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/subcontrato_views.xml',
        'data/cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}