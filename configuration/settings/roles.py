from rolepermissions.roles import AbstractUserRole


class APIUser(AbstractUserRole):
    available_permissions = {
        ('can_create_view_via_API', 'Create or View via API'),
        ('can_view_via_API', 'Create View only via API'),
    }
