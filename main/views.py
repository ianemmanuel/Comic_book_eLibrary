from django.shortcuts import render, redirect
from .models import Banner,Comic, Category, Publisher,CartOrder,CartOrderItems, ComicReview, Wishlist
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import math
from django.db.models import Max,Min,Count,Avg
from django.contrib.auth.decorators import login_required
from .forms import ReviewAdd, ComicForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
#download 
from django.template.loader import get_template
# from xhtml2pdf import pisa
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
#Recommendation
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


# Create your views here.
# Home Page
def home(request):
	banners=Banner.objects.all().order_by('-id')
	data=Comic.objects.filter(is_featured=True).order_by('-id')
	return render(request,'landing_page.html',{'data':data,'banners':banners})

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
	reviewForm = ReviewAdd()

	# Check
	canAdd = True
	reviewCheck = ComicReview.objects.filter(user=request.user, comic=comic).count()
	if request.user.is_authenticated:
		if reviewCheck > 0:
			canAdd = False
	# End

	# Fetch reviews
	reviews = ComicReview.objects.filter(comic=comic)
	# End

	# Fetch avg rating for reviews
	avg_reviews = ComicReview.objects.filter(comic=comic).aggregate(avg_rating=Avg('review_rating'))
	# End
	return render(request,'comic_detail.html',{'data':comic,'related':related_products, 'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

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

# Update Cart Item
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


#checkout
@login_required
def checkout(request):
	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			totalAmt+=math.ceil(int(item['qty'])*float(item['price']))
		# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items():
			total_amt+=math.ceil(int(item['qty'])*float(item['price']))
			# OrderItems
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
			# End
		# Process Payment
		host = request.get_host()
		paypal_dict = {
		    'business': settings.PAYPAL_RECEIVER_EMAIL,
		    'amount': total_amt,
		    'item_name': 'OrderNo-'+str(order.id),
		    'invoice': 'INV-'+str(order.id),
		    'currency_code': 'USD',
		    'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
		    'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
		    'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
		}
		form = PayPalPaymentsForm(initial=paypal_dict)
		# address=UserAddressBook.objects.filter(user=request.user,status=True).first()
		return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'form':form})

@csrf_exempt
def payment_done(request):
	returnData=request.POST
		#Process Payment
	# order_id='123'

	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			# total_amt+=int(item['qty'])*float(item['price'])
			pass
			# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
			# OrderItems
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
			# End
		comic=Comic.objects.get(pk=p_id)
		return render(request, 'payment-success.html',{'items':items,'comic':comic, 'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})




@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')

# Save Review
def save_review(request,pid):
	comic=Comic.objects.get(pk=pid)
	user=request.user
	review=ComicReview.objects.create(
		user=user,
		comic=comic,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}

	# Fetch avg rating for reviews
	avg_reviews=ComicReview.objects.filter(comic=comic).aggregate(avg_rating=Avg('review_rating'))
	# End

	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})


class AddComicView(CreateView):
	model = Comic
	form_class = ComicForm
	template_name = 'add_post.html'
	
class UpdateComicView(UpdateView):
	model = Comic
	template_name = 'update_post.html'
	form_class = ComicForm
	# fields = ['title','image','comicBook','detail','price','category','publisher']

class DeleteComicView(DeleteView):
	model = Comic
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')


def ticket_view(request,pid):
	comic=Comic.objects.get(pk=pid)
	comicBook = comic.comicBook
	
	template_path = 'pdf1.html'
	context = {'comic': comic}
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
	template = get_template(template_path)
	html = template.render(context)

	# # create a pdf
	# pisa_status = pisa.CreatePDF(
	# 		html, dest=response,)

	# if pisa_status.err:
	# 		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return comicBook




def recommendation(request):
	pid=request.GET['comic']
	comic=Comic.objects.get(pk=pid)
	wishlist=Wishlist.objects.filter(comic=comic, user=request.user).order_by('-id')

	checkw=Wishlist.objects.filter(comic=comic,user=request.user).count()

	# from google.colab import files
	# uploaded = files.upload()
	df = pd.read(wishlist)
	df.head(3)
	 # Get a count of the number of rows/ movies in the data set and the number of columns
	df.shape
		# Create a list of important columns for the recommendation engine
	columns = ['category', 'price','publisher','author','title']
		# Show the data
	df[columns].head(3)
		# Check for any missing values in the important columns
	df[columns].isnull().values.any()

	#	 Create a function to combine the values of the important columns into a single string
	def get_important_features(data):
		important_features = []
		for i in range(0, data.shape[0]):
			important_features.append(data['category'][i]+data['price'][i]+data['location'][i]+data['author'][i]+data['title'][i])
		return important_features

	df ['important_features'] = get_important_features(df)

	df.head(3)

	cm = CountVectorizer().fit_transform(df['important_features'])

# Get the cosine similarity matrix from the count matrix
	cs= cosine_similarity(cm)
	print(cs)
	
	cs.shape
	predictor_event = wishlist

	movie_id = df[df.title==predictor_event]['Event_id'].values[0]
	scores = list(enumerate(cs[movie_id]))
	sorted_scores = sorted(scores, key = lambda x:x[1], reverse = True)
	sorted_scores = sorted_scores[1:]
	print(sorted_scores)
	j = 0
	print('The 7 most recommended movies are: ')
	for item in sorted_scores:
		comic_title = df[df.Movie_id == item[0]]['title'].values[0]
		print(j+1, comic_title)
		j = j+1
		if j>4:
			break
	return render(request, 'comic_detail.html',{'comic_title':comic_title})
