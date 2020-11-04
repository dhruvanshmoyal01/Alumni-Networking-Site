from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
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
from .models import Profile, FollowUser
from django.db.models import Q
from django.db.models.query import QuerySet

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

    return render(request, 'user/profile.html', context)

def follow(request, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by=request.user)
    return HttpResponseRedirect('/profile_all')

class ProfileListView(ListView):
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

class ProfileDetailView(DetailView):
    model = Profile

def unfollow(request, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by=request.user).delete()
    return HttpResponseRedirect('/profile_all')

