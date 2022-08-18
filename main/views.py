from django.shortcuts import render
from .models import Banner,Comic

# Create your views here.

def home(request):
	banners=Banner.objects.all().order_by('-id')
	data=Comic.objects.filter(is_featured=True).order_by('-id')
	return render(request,'index.html',{'data':data,'banners':banners})
