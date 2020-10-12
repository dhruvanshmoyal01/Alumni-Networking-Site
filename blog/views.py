from django.shortcuts import render
from .models import Blog
from django.views.generic import ( ListView,
									DetailView,
									CreateView,
									UpdateView,
									DeleteView, 
								)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
def blogs(request):
	content = {
		'blogs' : Blog.objects.all(),
	}
	return render(request, 'blog/blogs.html', content)

class BlogListView(ListView):
	model = Blog
	template_name = 'blog/blogs.html'
	context_object_name = 'blogs'
	queryset = Blog.objects.order_by('-date_posted')

class BlogDetailView(DetailView):
	model = Blog

class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Blog
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Blog
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		blog = self.get_object()
		if self.request.user == blog.author:
			return True
		return False

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Blog
	success_url = '/blogs'
	
	def test_func(self):
		blog = self.get_object()
		if self.request.user == blog.author:
			return True
		return False