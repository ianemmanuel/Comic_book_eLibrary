from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('category-list',views.category_list,name='category-list'),
    path('publisher-list',views.publisher_list,name='publisher-list'),
    path('comic-list',views.comic_list,name='comic-list'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)