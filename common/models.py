from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class News(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	pic = models.ImageField(upload_to='news_pic', default='blog-post.jpg')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('news-detail', kwargs={'pk':self.pk})

class Event(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	date_of_event = models.DateField()
	venue = models.TextField()
	time = models.CharField(max_length=50, null=True, blank=True)
	pic = models.ImageField(upload_to='event_pic', null=True, blank=True)
	organizing_committee = models.CharField(max_length=50, null=True, blank=True)
	phone_number = models.CharField(max_length=50, null=True, blank=True)
	email = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('events-detail', kwargs={'pk':self.pk})

class UserQuery(models.Model):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	message = models.TextField()

	def __str__(self):
		return self.subject
