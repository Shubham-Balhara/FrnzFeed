from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
	photo = models.FileField()
	phone_no = models.IntegerField()
	status = models.CharField(max_length=1000)

	def ___str__(self):
		return self.phone_no

class Post(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	pic = models.FileField()
	quote = models.CharField(max_length=3000)
	likes = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)

	def ___str__(self):
		return self.pk

class Friend(models.Model):
	name = models.CharField(max_length=300)
	user = models.ManyToManyField(User)

	def ___str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('friends',args=[str(self.id)])

class Rqst(models.Model):
	receiver = models.CharField(max_length=300)
	sender = models.CharField(max_length=300)

	def ___str__(self):
		return self.sender + '-' + self.receiver

class Like(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	user_id = models.IntegerField(default=None)

class Clients(models.Model):
	name = models.CharField(max_length=300)
	ch_name = models.CharField(max_length=1000)

	def ___str__(self):
		return self.name

class Messages(models.Model):
	to = models.CharField(max_length=300)
	frm = models.CharField(max_length=300)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def ___str__(self):
		return self.to+'-'+self.frm

class Comments(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	user = models.CharField(max_length=300,default='admin')
	comment = models.TextField()
	date = models.DateTimeField(auto_now_add=True,null=True)

	def ___str__(self):
		return self.comment