from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from demo_register import settings
from django.urls import reverse

from ckeditor.fields import RichTextField

# Create your models here.
class Banner(models.Model):
    img = models.ImageField(upload_to="banner_imgs/")
    alt_text= models.CharField(max_length=32)

    class Meta:
        verbose_name_plural='1. Banners'

    
    def image_tag(self):
        return mark_safe('<img src="%s" width="70" />' % (self.img.url))

    def __str__(self):
        return self.alt_text


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_imgs/")


    class Meta:
        verbose_name_plural='2. Categories'
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.image.url))

    def __str__(self):
        return self.title

class Publisher(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="pub_imgs/")


    class Meta:
        verbose_name_plural='3.Publishers'

    def __str__(self):
        return self.title

class Comic(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="comic_imgs/")
    comicBook = models.FileField(upload_to='comic_files/')
    slug  = models.CharField(max_length=400,default=title)
    # detail= models.TextField()
    detail=RichTextField(blank=True, null=True)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE) 
    status = models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)
    vendor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)



    class Meta:
        verbose_name_plural='4.Comics'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('comic_detail', args=(str(self.id)))
        return reverse('home')



class CartOrder(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural='5. Orders'

# OrderItems
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='6. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


# Comic Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ComicReview(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comic=models.ForeignKey(Comic,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural=' 7. Reviews'

    def get_review_rating(self):
        return self.review_rating


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    bio=models.TextField()
    profile_pic = models.ImageField(upload_to="profile_imgs/",null=True, blank=True)
    facebook_url=models.CharField(max_length=200, blank=True, null=True)
    instagram_url=models.CharField(max_length=200, blank=True, null=True)
    twitter_url=models.CharField(max_length=200, blank=True, null=True)
    website_url=models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural='8. Profile'

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')