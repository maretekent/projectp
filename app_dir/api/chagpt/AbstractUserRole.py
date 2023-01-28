from django.db import models


class AbstractUserRole(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()

	class Meta:
		abstract = True


class UserRole(AbstractUserRole):
	pass


from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)


# Create a new role via the shell
from myapp.models import UserRole

admin_role = UserRole.objects.create(name="admin", description="Administrator role")


user = CustomUser.objects.get(username="johndoe")
user.role = admin_role
user.save()
