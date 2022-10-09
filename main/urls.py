from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('category-list',views.category_list,name='category-list'),
    path('publisher-list',views.publisher_list,name='publisher-list'),
    path('comic-list',views.comic_list,name='comic-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('publisher-comic-list/<int:publisher_id>',views.publisher_comic_list,name='publisher-comic-list'),
    path('comic/<str:slug>/<int:id>',views.comic_detail,name='comic_detail'),
     path('load-more-data',views.load_more_data,name='load_more_data'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)