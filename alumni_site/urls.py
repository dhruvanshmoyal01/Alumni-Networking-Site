"""alumni_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from common import views as common_views
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', common_views.index, name='index-page'),
    path('about/', common_views.aboutUs, name='about'),
    path('common/news/', common_views.NewsListView.as_view(), name = 'news-home'),
    path('common/news/<int:pk>/', common_views.NewsDetailView.as_view(), name = 'news-detail'),
    path('common/events/<int:pk>/', common_views.EventDetailView.as_view(), name = 'events-detail'),
    path('grievance/', common_views.grievance, name = 'user-grievance'),
    path('', common_views.userQuery, name = 'user-query'),
    
    path('blogs/', include('blog.urls')),
    path('posts/', include('post.urls')),

    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name = 'logout'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/update/', user_views.profileUpdate, name='profile-update'),
    path('profile_all/', user_views.ProfileListView.as_view(), name='profile-list'),
    path('profile_all/<int:pk>/', user_views.ProfileDetailView.as_view(), name = 'profile-detail'),
    path('profile_all/follow/<int:pk>/', user_views.follow, name = 'follow-user'),
    path('profile_all/unfollow/<int:pk>/', user_views.unfollow, name = 'unfollow-user'),
    path('my_activity/', user_views.myactivity, name = 'my-acivity'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)