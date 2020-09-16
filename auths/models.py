from django.db import models
from django.contrib.auth.models import User


class Interest(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name
	
		


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	alcher_id = models.CharField(max_length=20, default="temp")
	fullname = models.CharField(max_length=200)
	phone = models.CharField(max_length=11)
	college = models.CharField(max_length=100)
	GENDER_CHOICES = [
	('M', 'Male'),
	('F', 'Female'),
	]
	gender = models.CharField(
		choices = GENDER_CHOICES,
		max_length=1,
		default='M'
		)
	state = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=100, blank=True)
	interests = models.ManyToManyField(Interest)
	emailVerified = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username


class CA_Detail(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ca_details')
	ca_profile_complete = models.BooleanField(default=False)
	ca_approval = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	score = models.IntegerField(default=0)
	triweekly=models.IntegerField(default=0,verbose_name='Tri-weekly score')

	def __str__(self):
		return f'{self.user.username} ca_detail '