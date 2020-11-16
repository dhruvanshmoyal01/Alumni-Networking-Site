from django.contrib import admin
from .models import News, Event, UserQuery

# Register your models here.
admin.site.register(News)
admin.site.register(Event)
admin.site.register(UserQuery)