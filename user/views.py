from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ( UserRegisterForm,
					 UserUpdateForm,
					 ProfileUpdateForm
					)
from django.views.generic import ( ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView, 
                                )
from django.contrib.auth.models import User
from .models import Profile, FollowUser
from django.db.models import Q
from django.db.models.query import QuerySet
from blog.models import Blog, Blog_upvote
from post.models import Post, Post_upvote

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account Created for {username}!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'user/register.html', {'form' : form})

@login_required
def profile(request):
    #if request.method == 'POST':
    #    u_form = UserUpdateForm(request.POST, instance=request.user)
    #    p_form = ProfileUpdateForm(request.POST,
    #                               request.FILES,
    #                               instance=request.user.profile)
    #    if u_form.is_valid() and p_form.is_valid():
    #        u_form.save()
    #        p_form.save()
    #        messages.success(request, f'Your account has been updated!')
    #        return redirect('profile')
    #
    #else:
    #    u_form = UserUpdateForm(instance=request.user)
    #    p_form = ProfileUpdateForm(instance=request.user.profile)

    #context = {
    #    'u_form': u_form,
    #    'p_form': p_form
    #}
    blog = Blog.objects.filter(Q(author = request.user)).order_by("-date_posted")
    posts = Post.objects.filter(Q(author = request.user)).order_by("-date_posted")
  
    blog_upvotes = 0
    post_upvotes = 0

    for p in posts:
      p.liked = False
      ob = Post_upvote.objects.filter(post=p, upvote_by=request.user)
      if ob:
        p.liked = True
      upvotes = Post_upvote.objects.filter(post=p)
      p.upvote_count = upvotes.count()
      post_upvotes += Post_upvote.objects.filter(post=p).count()
    
    followers = FollowUser.objects.filter(Q(profile=request.user.profile)).count()
    following = FollowUser.objects.filter(Q(followed_by=request.user)).count()
   
    for b in blog:
      blog_upvotes += Blog_upvote.objects.filter(blog=b).count()

    total_upvotes = blog_upvotes+post_upvotes
    if following==0:
      rating = 1
    else:
      rating = round((followers/following)*10, 1)
    context = {
        'user' : request.user,
        'blogs' : blog,
        'posts' : posts,
        'followers' : followers,
        'following' : following,
        'rating' : rating,
        'total_upvotes' : total_upvotes
    }
    return render(request, 'user/profile.html', context)

def profileUpdate(request):
    if request.method == 'POST':
      u_form = UserUpdateForm(request.POST, instance=request.user)
      p_form = ProfileUpdateForm(request.POST,
                                 request.FILES,
                                 instance=request.user.profile)
      if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Your account has been updated!')
        return redirect('profile')
    
    else:
      u_form = UserUpdateForm(instance=request.user)
      p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
      'u_form': u_form,
      'p_form': p_form
    }
    return render(request, 'user/profile_update.html', context)


def follow(request, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by=request.user)
    return HttpResponseRedirect('/profile_all')

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'user/profile_list.html'
    context_object_name = 'profile'
    
    def get_queryset(self):
        q = self.request.GET.get("q")
        if q == None:
            q = ""
        profileList = Profile.objects.filter(Q(user__username__icontains = q)).order_by("-id")
        for p in profileList:
            p.followed = False
            ob = FollowUser.objects.filter(profile=p, followed_by=self.request.user)
            if ob:
                p.followed = True
        return profileList

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
      context = {}
      o = self.get_object()
      blog = Blog.objects.filter(Q(author = o.user)).order_by("-date_posted")
      posts = Post.objects.filter(Q(author = o.user)).order_by("-date_posted")

      blog_upvotes = 0
      post_upvotes = 0

      for p in posts:
        p.liked = False
        ob = Post_upvote.objects.filter(post=p, upvote_by=o.user)
        if ob:
          p.liked = True
        upvotes = Post_upvote.objects.filter(post=p)
        p.upvote_count = upvotes.count()
        post_upvotes += Post_upvote.objects.filter(post=p).count()
      
      followers = FollowUser.objects.filter(Q(profile=o)).count()
      following = FollowUser.objects.filter(Q(followed_by=o.user)).count()
     
      for b in blog:
        blog_upvotes += Blog_upvote.objects.filter(blog=b).count()

      total_upvotes = blog_upvotes+post_upvotes
      if following==0:
        rating = 1
      else:
        rating = round((followers/following)*10, 1)
      followed = False
      followedList = FollowUser.objects.filter(profile = o, followed_by = self.request.user)
      if followedList:
        followed = True

      context = {
          'profile': o,
          'blogs' : blog,
          'posts' : posts,
          'followers' : followers,
          'following' : following,
          'rating' : rating,
          'total_upvotes' : total_upvotes,
          'followed' : followed
      }
      return context



def unfollow(request, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by=request.user).delete()
    return HttpResponseRedirect('/profile_all')

@login_required
def userSearch(request):
  if request.method == 'POST':
    usrname = request.POST['iodata']
    ob = User.objects.filter(username=usrname)
    plist = []
    for o in ob:
      plist.append(o.profile)
    context={
      'profile' : plist 
    }
    return render(request, 'user/profile_list.html', context)
  else:
    return render(request, 'user/userSearch.html')