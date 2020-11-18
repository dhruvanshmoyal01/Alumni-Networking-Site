from django.shortcuts import render
from .models import Blog, Blog_upvote, Blog_comment
from django.views.generic import ( ListView,
									DetailView,
									CreateView,
									UpdateView,
									DeleteView, 
								)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from user.models import FollowUser
from django.http import HttpResponseRedirect

# Create your views here.
@login_required
def blogs(request):
	content = {
		'blogs' : Blog.objects.all(),
	}
	return render(request, 'blog/blogs.html', content)

class BlogListView(LoginRequiredMixin, ListView):
	model = Blog
	template_name = 'blog/blogs.html'
	
	def get_context_data(self, **kwargs):
		context = ListView.get_context_data(self, **kwargs)
		followedList = FollowUser.objects.filter(followed_by = self.request.user)
		followedList2 = []
		for e in followedList:
			followedList2.append(e.profile.user)
		q = self.request.GET.get("q")
		if q == None:
			q = ""
		blogs = Blog.objects.filter(Q(author__in = followedList2)).order_by("-date_posted")
		#for p in blogs:
		#	p.liked = False
		#	ob = Blog_upvote.objects.filter(blog=p, upvote_by=self.request.user)
		#	if ob:
		#		p.liked = True
		#	upvotes = Blog_upvote.objects.filter(blog=p)
		#	p.upvote_count = upvotes.count()	
		context["blogs"] = blogs
		return context


class BlogDetailView(LoginRequiredMixin, DetailView):
	model = Blog

	def get_context_data(self, **kwargs):
		context = {}
		o = self.get_object()
		o.liked = False
		ob = Blog_upvote.objects.filter(blog=o, upvote_by=self.request.user)
		if ob:
			o.liked = True
		upvotes = Blog_upvote.objects.filter(blog=o)
		o.upvote_count = upvotes.count()	
		o.comments = Blog_comment.objects.filter(blog=o).order_by('-date_posted')
		context['blog'] = o
		return context

class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Blog
	fields = ['title', 'content', 'tag', 'cover_pic']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Blog
	fields = ['title', 'content', 'tag', 'cover_pic']

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

def upvote(self, pk):
	blog = Blog.objects.get(pk=pk)
	Blog_upvote.objects.create(blog=blog, upvote_by=self.user)
	return HttpResponseRedirect('/blogs/blog/{}'.format(pk))

def devote(self, pk):
	blog = Blog.objects.get(pk=pk)
	Blog_upvote.objects.filter(blog=blog, upvote_by=self.user).delete()
	return HttpResponseRedirect('/blogs/blog/{}'.format(pk))

def blog_comment(request, pk):
	blog = Blog.objects.get(pk=pk)
	msg = request.POST['msg']
	Blog_comment.objects.create(blog=blog, msg=msg, commented_by=request.user)
	return HttpResponseRedirect('/blogs/blog/{}'.format(pk))

class BlogListTagView(LoginRequiredMixin, ListView):
	model = Blog
	template_name = 'blog/blogs.html'
	
	def get_context_data(self, **kwargs):
		context = ListView.get_context_data(self, **kwargs)
		followedList = FollowUser.objects.filter(followed_by = self.request.user)
		followedList2 = []
		for e in followedList:
			followedList2.append(e.profile.user)
		q = self.request.GET.get("q")
		if q == None:
			q = ""
		blogs = Blog.objects.filter(Q(author__in = followedList2)).order_by("-date_posted")
		#for p in blogs:
		#	p.liked = False
		#	ob = Blog_upvote.objects.filter(blog=p, upvote_by=self.request.user)
		#	if ob:
		#		p.liked = True
		#	upvotes = Blog_upvote.objects.filter(blog=p)
		#	p.upvote_count = upvotes.count()	
		context["blogs"] = blogs
		return context

@login_required
def blogs_tag(request, tag):
	followedList = FollowUser.objects.filter(followed_by = request.user)
	followedList2 = []
	for e in followedList:
		followedList2.append(e.profile.user)
	q = request.GET.get("q")
	if q == None:
		q = ""
	blogs = Blog.objects.filter(Q(author__in = followedList2), tag = tag).order_by("-date_posted")
	print(blogs)
	content = {
		'blogs' : blogs,
	}
	return render(request, 'blog/blogs.html', content)