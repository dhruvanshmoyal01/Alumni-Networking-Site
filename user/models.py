from django.db import models
from django.contrib.auth.models import User 
from PIL import Image
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pic')
	age = models.IntegerField(default = 18, validators = [MinValueValidator(18)])
	phone_number = models.CharField(validators = [RegexValidator("^0?[5-9]{1}\d{9}$")], max_length = 15, null = True, blank = True)
	bio = models.TextField(null = True, blank = True)
	address = models.TextField(max_length=200, null=True, blank=True)
	status = models.CharField(max_length=20, default='student', choices=(('Employee', 'Employee'), ('Freelancer', 'Freelancer'), ('Entreprenur', 'Entreprenur'), ('Student', 'Student'), ('Professor', 'Professor')))
	gender = models.CharField(max_length=20, default='male', choices=(('male', 'male'), ('female', 'female'), ('other', 'other')))

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
	    super(Profile, self).save(*args, **kwargs)

	    img = Image.open(self.image.path)

	    if img.height > 300 or img.width > 300:
	        output_size = (300,300)
	        img.thumbnail(output_size)
	        img.save(self.image.path)

class FollowUser(models.Model):
	profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="profile")
	followed_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="followed_by")

	def __str__(self):
		return f'{self.followed_by}'
		