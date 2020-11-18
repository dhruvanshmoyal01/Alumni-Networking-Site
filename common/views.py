from django.shortcuts import render
from django.http import HttpResponse
from .models import News, Event, UserQuery
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
	content = {
		'news' : News.objects.all().order_by('date_posted'),
		'events' : Event.objects.all().order_by('date_of_event'),
	}
	return render(request, 'common/index.html', content)

def aboutUs(request):
	return render(request, 'common/aboutus.html')

class NewsListView(ListView):
	model = News
	template_name = 'common/news.html'
	queryset = News.objects.order_by('date_posted')

	def get_context_data(self, **kwargs):
		context = ListView.get_context_data(self, **kwargs)
		context['news'] = News.objects.all().order_by('-date_posted')
		context['events'] = Event.objects.all().order_by('date_of_event')
		return context

class NewsDetailView(DetailView):
	model = News


class EventListView(ListView):
	model = Event
	template_name = 'common/events.html'
	context_object_name = 'events'
	queryset = Event.objects.order_by('-date_of_event')

class EventDetailView(DetailView):
	model = Event

def grievance(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		subject = request.POST['subject']
		message = request.POST['message']
		UserQuery.objects.create(name=name, email=email, subject=subject, message=message)
		messages.success(request, f'Query Recieved!')
		return HttpResponseRedirect('..')
	else:
		return render(request, 'common/grievance_form.html')

def userQuery(request):
	name = request.POST['name']
	email = request.POST['email']
	subject = request.POST['subject']
	message = request.POST['message']
	UserQuery.objects.create(name=name, email=email, subject=subject, message=message)
	messages.success(request, f'Query Recieved!')
	return render(request, 'common/index.html')

	