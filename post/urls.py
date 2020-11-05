from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', PostListView.as_view(), name = 'post-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/<int:pk>/upvote/', views.upvote, name = 'post-upvote'),
    path('post/<int:pk>/devote/', views.devote, name = 'post-devote'),
    path('post/<int:pk>/comment/', views.post_comment, name = 'post-comment'),
]
