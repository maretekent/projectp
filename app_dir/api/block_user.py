class User(AbstractBaseUser, PermissionsMixin):
	"""
	An abstract base class implementing a fully featured User model with
	admin-compliant permissions.

	"""
	user_type = [
		('AD', 'Administrator'),
		('AN', 'Analyst'),
		('AU', 'Auditor'),
		('MA', 'Management'),
		('SA', 'SAR Team'),
		('UA', 'User Administrator'),
	]

	email = models.EmailField(max_length=40, unique=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	logged_in = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)
	notification_flag = models.BooleanField(default=True)
	user_group = models.CharField(max_length=2, blank=False, default='UA', choices=user_type)
	previous_login = models.IntegerField(default=0, blank=True, null=True)
	profile_pic = models.ImageField(upload_to="accounts/images/", null=True, blank=True)
	adverse_media = models.BooleanField(default=False)
	customer_adverse_media = models.BooleanField(default=False)
	admin_adverse_media = models.BooleanField(default=False)
	objects = UserManager()
	history = HistoricalRecords()
	user_rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'user_group']

	def save(self, *args, **kwargs):
		super(User, self).save(*args, **kwargs)
		return self

	def has_perm(self, perm, obj=None):
		# check if user has permission
		perm_label, perm_code = perm.split('.')
		queryset = self.get_user_permissions()
		return self.is_superuser or perm_code in [p.codename for p in queryset] or self.groups.filter(
			permissions__codename=perm_code).exists()

	def has_module_perms(self, app_label):
		# check if user has permission for app
		return self.is_superuser or self.groups.filter(
			permissions__content_type__app_label=app_label).exists()

	def get_user_permissions(self):
		# get all permissions for user
		return Permission.objects.filter(
			Q(group__user=self) | Q(user=self)).distinct()

	@property
	def name(self):
		return '{} {}'.format(self.first_name, self.last_name)

	@property
	def get_groups(self):
		# get all groups for user
		return self.groups.all()

	@property
	def get_permissions(self):
		# get all permissions for user
		return Permission.objects.filter(
			Q(group__user=self) | Q(user=self)).distinct()
