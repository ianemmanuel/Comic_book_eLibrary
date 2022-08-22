from .models import Comic, Category, Publisher
from django.db.models import Min,Max

def get_filters(request):
	# cats=Comic.objects.distinct().values('category__title','category__id')
    cats=Category.objects.all().order_by('-id')
	# publishers=Comic.objects.distinct().values('publisher__title','publisher__id')
    publishers= Publisher.objects.all().order_by('-id')

    data={
		'cats':cats,
		'publishers':publishers,
	}

    return data
	
	
	