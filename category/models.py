from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255)
    category_image = models.ImageField(upload_to='media/categories', blank=True)

    def __str__(self):
        return str(self.category_name)



