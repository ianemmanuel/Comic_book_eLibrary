from django.shortcuts import render
from .models import Banner,Comic, Category, Publisher
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import math
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
	total_data=Comic.objects.count()
	data=Comic.objects.all().order_by('-id')[:3]
	
	return render(request,'comic_list.html',
	{
		'data':data,
		'total_data':total_data,
	
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


# Filter Data
def filter_data(request):
	
	categories=request.GET.getlist('category[]')
	publishers=request.GET.getlist('publisher[]')
	
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Comic.objects.all().order_by('-id').distinct()
	
	
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(publishers)>0:
		allProducts=allProducts.filter(publisher__id__in=publishers).distinct()
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Comic.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data})
	return JsonResponse({'data':t})

# Add to cart
def add_to_cart(request):
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

#cart-list
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt+=math.ceil(int(item['qty'])*float(item['price']))
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# Delete Cart Item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=math.ceil(int(item['qty'])*float(item['price']))
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})
