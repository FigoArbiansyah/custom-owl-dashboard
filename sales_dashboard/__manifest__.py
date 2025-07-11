{
    'name': 'Sales Dashboard',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'author': "Figo Arbiansyah",
    'website': "https://www.figo.my.id",
    'summary': 'Custom Sales Order Dashboard with OWL JS',
    'description': """
        Custom Dashboard untuk Sales Order dengan fitur:
        - Ringkasan penjualan per periode
        - Total omzet
        - Status order (processed, pending, cancelled)
    """,
    'depends': ['base', 'sale', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_dashboard_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sales_dashboard/static/src/js/sales_dashboard.js',
            'sales_dashboard/static/src/xml/sales_dashboard.xml',
            'sales_dashboard/static/src/css/sales_dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}

