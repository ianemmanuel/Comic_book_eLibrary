from django.contrib import admin
from .models import Category, Publisher,Comic,Banner

# Register your models here.
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Publisher)


class ComicAdmin(admin.ModelAdmin):
    list_display=('id','title','price','category','publisher','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Comic,ComicAdmin)