from django.contrib import admin
from .models import Blog, Blog_upvote, Blog_comment

# Register your models here.
admin.site.register(Blog)
admin.site.register(Blog_comment)
admin.site.register(Blog_upvote)