from django.urls import path
from . import views
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView


urlpatterns = [
    path('', BlogListView.as_view(), name = 'blog-home'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name = 'blog-detail'),
    path('blog/new/', BlogCreateView.as_view(), name = 'blog-create'),
    path('blog/<int:pk>/update', BlogUpdateView.as_view(), name = 'blog-update'),
    path('blog/<int:pk>/delete', BlogDeleteView.as_view(), name = 'blog-delete'),
    path('blog/<int:pk>/upvote/', views.upvote, name = 'blog-upvote'),
    path('blog/<int:pk>/devote/', views.devote, name = 'blog-devote'),
    path('blog/<int:pk>/comment/', views.blog_comment, name = 'blog-comment'),
]
