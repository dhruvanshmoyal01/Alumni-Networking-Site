from django.contrib import admin
from .models import Post, Post_upvote, Post_comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Post_comment)
admin.site.register(Post_upvote)