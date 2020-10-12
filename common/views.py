from django.shortcuts import render
from django.http import HttpResponse
from .models import News
from django.views.generic import ListView, DetailView

# Create your views here.
def index(request):
	content = {
		'news' : News.objects.all(),
	}
	return render(request, 'common/index.html', content)

class NewsListView(ListView):
	model = News
	template_name = 'common/news.html'
	context_object_name = 'news'
	queryset = News.objects.order_by('-date_posted')

class NewsDetailView(DetailView):
	model = News
