from django.shortcuts import render
from .models import Post, Post_upvote, Post_comment
from django.views.generic import ( ListView,
									DetailView,
									CreateView,
									UpdateView,
									DeleteView, 
								)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.db.models import Q
from user.models import FollowUser
from django.http import HttpResponseRedirect

# Create your views here.
def posts(request):
	content = {
		'posts' : Post.objects.all(),
	}
	return render(request, 'post/posts.html', content)

class PostListView(ListView):
	model = Post
	template_name = 'post/posts.html'
	
	def get_context_data(self, **kwargs):
		context = ListView.get_context_data(self, **kwargs)
		followedList = FollowUser.objects.filter(followed_by = self.request.user)
		followedList2 = []
		for e in followedList:
			followedList2.append(e.profile.user)
		q = self.request.GET.get("q")
		if q == None:
			q = ""
		posts = Post.objects.filter(Q(author__in = followedList2)).order_by("-date_posted")
		#for p in blogs:
		#	p.liked = False
		#	ob = Blog_upvote.objects.filter(blog=p, upvote_by=self.request.user)
		#	if ob:
		#		p.liked = True
		#	upvotes = Blog_upvote.objects.filter(blog=p)
		#	p.upvote_count = upvotes.count()	
		context["posts"] = posts
		return context

class PostDetailView(DetailView):
	model = Post

	def get_context_data(self, **kwargs):
		context = {}
		o = self.get_object()
		o.liked = False
		ob = Post_upvote.objects.filter(post=o, upvote_by=self.request.user)
		if ob:
			o.liked = True
		upvotes = Post_upvote.objects.filter(post=o)
		o.upvote_count = upvotes.count()
		o.comments = Post_comment.objects.filter(post=o)
		context['post'] = o
		return context

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

def upvote(self, pk):
	post = Post.objects.get(pk=pk)
	Post_upvote.objects.create(post=post, upvote_by=self.user)
	return HttpResponseRedirect('/posts/post/{}'.format(pk))

def devote(self, pk):
	post = Post.objects.get(pk=pk)
	Post_upvote.objects.filter(post=post, upvote_by=self.user).delete()
	return HttpResponseRedirect('/posts/post/{}'.format(pk))

def post_comment(request, pk):
	post = Post.objects.get(pk=pk)
	msg = request.POST['msg']
	Post_comment.objects.create(post=post, msg=msg, commented_by=request.user)
	return HttpResponseRedirect('/posts/post/{}'.format(pk))