from django.db import models
from django.utils.html import mark_safe

# Create your models here.
class Banner(models.Model):
    img = models.CharField(max_length=200)
    alt_text= models.CharField(max_length=32)

    class Meta:
        verbose_name_plural='1. Banners'


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
    slug  = models.CharField(max_length=400)
    detail= models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE) 
    status = models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)


    class Meta:
        verbose_name_plural='4.Comics'


    def __str__(self):
        return self.title