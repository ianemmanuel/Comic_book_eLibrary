from django.urls import path,include
from . import views
from .views import *

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
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('checkout',views.checkout,name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    path('add_post/', AddComicView.as_view(), name='add_post'),
    path('update-comic/<int:pk>', UpdateComicView.as_view(), name='update_comic'),
    path('delete-comic/<int:pk>', DeleteComicView.as_view(), name='delete_comic'),
   
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)