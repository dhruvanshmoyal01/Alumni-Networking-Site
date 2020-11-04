from django.shortcuts import render
from .models import Post
from django.views.generic import ( ListView,
									DetailView,
									CreateView,
									UpdateView,
									DeleteView, 
								)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

# Create your views here.
def posts(request):
	content = {
		'posts' : Post.objects.all(),
	}
	return render(request, 'post/posts.html', content)

class PostListView(ListView):
	model = Post
	template_name = 'post/posts.html'
	context_object_name = 'posts'
	queryset = Post.objects.order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['subject', 'msg', 'pic']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['subject', 'msg', 'pic']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/posts'
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False