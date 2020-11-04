from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class News(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('news-detail', kwargs={'pk':self.pk})
