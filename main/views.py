from django.shortcuts import render
from .models import Banner,Comic, Category, Publisher
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
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
		
# Comic-list according to category
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=Comic.objects.filter(category=category).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})

# Product List According to Brand
def publisher_comic_list(request,publisher_id):
	publisher=Publisher.objects.get(id=publisher_id)
	data=Comic.objects.filter(publisher=publisher).order_by('-id')
	return render(request,'publisher_comic_list.html',{
			'data':data,
			})


# Product Detail
def comic_detail(request,slug,id):
	comic=Comic.objects.get(id=id)
	related_products=Comic.objects.filter(category=comic.category).exclude(id=id)[:4]
	return render(request,'comic_detail.html',{'data':comic,'related':related_products})

# Search
def search(request):
	q=request.GET['q']
	data=Comic.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})


# # Filter Data
# def filter_data(request):
	
# 	categories=request.GET.getlist('category[]')
# 	publishers=request.GET.getlist('publisher[]')
	
# 	minPrice=request.GET['minPrice']
# 	maxPrice=request.GET['maxPrice']
# 	allProducts=Comic.objects.all().order_by('-id').distinct()
	
	
# 	if len(categories)>0:
# 		allProducts=allProducts.filter(category__id__in=categories).distinct()
# 	if len(publishers)>0:
# 		allProducts=allProducts.filter(publisher__id__in=publishers).distinct()
# 	t=render_to_string('ajax/product-list.html',{'data':allProducts})
# 	return JsonResponse({'data':t})

