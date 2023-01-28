from rolepermissions.roles import AbstractUserRole


class APIUser(AbstractUserRole):
	available_permissions = {
		('can_create_view_via_API', 'Create or View via API'),
		('can_view_via_API', 'Create View only via API'),
	}


class Doctor(AbstractUserRole):
	available_permissions = {
		'create_medical_record': True,
	}


class Nurse(AbstractUserRole):
	available_permissions = {
		'edit_patient_file': True,
	}


class SystemAdmin(AbstractUserRole):
	available_permissions = {
		'drop_tables': True,
	}
