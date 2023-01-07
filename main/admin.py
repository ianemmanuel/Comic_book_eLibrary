from django.contrib import admin
from .models import Category, Publisher,Comic,Banner, CartOrder,CartOrderItems, ComicReview, Wishlist

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

# Order
class CartOrderAdmin(admin.ModelAdmin):
	# list_editable=('paid_status')
	list_display=('user','total_amt','paid_status','order_dt')
admin.site.register(CartOrder,CartOrderAdmin)


class CartOrderItemsAdmin(admin.ModelAdmin):
	list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)


class ComicReviewAdmin(admin.ModelAdmin):
	list_display=('user','comic','review_text','get_review_rating')
admin.site.register(ComicReview,ComicReviewAdmin)


admin.site.register(Wishlist)