from django.contrib import admin
from .models import Category, Publisher,Comic,Banner

# Register your models here.

admin.site.register(Publisher)


class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ComicAdmin(admin.ModelAdmin):
    list_display=('id','title','price','category','publisher','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Comic,ComicAdmin)

class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)