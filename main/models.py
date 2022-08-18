from django.db import models

# Create your models here.
class Banner(models.Model):
    img = models.CharField(max_length=200)
    alt_text= models.CharField(max_length=32)


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_imgs/")

    def __str__(self):
        return self.title

class Publisher(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="pub_imgs/")

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


    def __str__(self):
        return self.title