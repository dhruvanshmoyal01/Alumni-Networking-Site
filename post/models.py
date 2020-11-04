from django.db import models
from django.contrib.auth.models import User 
from PIL import Image
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
	pic = models.ImageField(upload_to='post_pic')
	subject = models.CharField(max_length=200)
	msg = models.TextField(null=True, blank=True)
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.subject

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})

class Post_comment(models.Model):
	post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
	msg = models.TextField()
	commented_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default = timezone.now)
	flag = models.CharField(max_length=20, null=True, blank=True, choices=(('abusive', 'abusive'), ('inappropriate', 'inappropriate'), ('other', 'other')))

	def __str__(self):
		return self.msg

class Post_upvote(models.Model):
	post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
	upvote_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default = timezone.now)
	
	def __str__(self):
		return self.upvote.username