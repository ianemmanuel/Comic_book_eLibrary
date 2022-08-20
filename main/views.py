from django.shortcuts import render
from .models import Banner,Comic, Category, Publisher

# Create your views here.
# Home Page
def home(request):
	banners=Banner.objects.all().order_by('-id')
	data=Comic.objects.filter(is_featured=True).order_by('-id')
	return render(request,'index.html',{'data':data,'banners':banners})

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})

# Publisher
def publisher_list(request):
    data=Publisher.objects.all().order_by('-id')
    return render(request,'publisher_list.html',{'data':data})

# Comic-list

def comic_list(request):
	data=Comic.objects.all().order_by('-id')
	# cats=Comic.objects.distinct().values('category__title','category__id')
	cats=Category.objects.all().order_by('-id')
	# publishers=	Comic.objects.distinct().values('publisher__title','publisher__id')
	publishers= Publisher.objects.all().order_by('-id')
	return render(request,'comic_list.html',
	{
		'data':data,
		'cats':cats,
		'publishers':publishers,
	
	})
		
