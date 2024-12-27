# permissions_config.py

permissions_mapping = {
    'Country': {
        'admin': ['create', 'read', 'update', 'delete'],
        'employee': ['create', 'read', 'update'],
    },
    'Model1': {
        'admin': ['create', 'read', 'update', 'delete'],
        'employee': ['create', 'read'],
        'student': ['read'],
    },
    'Model2': {
        'admin': ['create', 'read', 'update', 'delete'],
        'employee': ['create', 'read'],
        'instructor': ['read', 'update'],
    },
    'Model3': {
        'admin': ['create', 'read', 'update', 'delete'],
        'employee': ['create', 'read'],
        'anonymous': ['read'],  # 'anonymous' for non-authenticated users
    },
    # Future models can be added here
}
