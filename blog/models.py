from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Blog(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	tag = models.CharField(max_length=20, null=True, blank=True, choices=(('web-design', 'web-design'), ('html', 'html'), ('css', 'css'), ('freebies', 'freebies'), ('tutorials', 'tutorials')))
	cover_pic = models.ImageField(upload_to='blog-cover', default='blog-post.jpg')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog-detail', kwargs={'pk':self.pk})

class Blog_comment(models.Model):
	blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
	msg = models.TextField()
	commented_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default = timezone.now)
	flag = models.CharField(max_length=20, null=True, blank=True, choices=(('abusive', 'abusive'), ('inappropriate', 'inappropriate'), ('other', 'other')))

	def __str__(self):
		return self.msg

class Blog_upvote(models.Model):
	blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
	upvote_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default = timezone.now)
	
	def __str__(self):
		return self.upvote_by.username