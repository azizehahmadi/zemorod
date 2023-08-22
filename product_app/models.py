import os.path
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from user_app.models import User
import uuid

def url_upload_image_product(instance, data):
    exe = data.split('.')[-1]
    image_data = f'{uuid.uuid4()}.{exe}'
    return os.path.join('upload/product/', image_data)

class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='title')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', default=False)
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده', null=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='title')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='category')
    price = models.IntegerField(verbose_name="price")
    short_description = models.CharField(null=True, db_index=True, verbose_name="description", max_length=360)
    description = models.TextField(verbose_name="main description", db_index=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name="active/inactive", null=True)
    is_delete = models.BooleanField(verbose_name='deleted', null=True)
    image = models.ImageField(upload_to=url_upload_image_product, null=True, blank=True, verbose_name='image')
    date_register = models.DateField(verbose_name='date of add product')
    def __str__(self):
        return f"{self.title}({self.price})"


class RatingProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    comment = models.TextField()
    ip = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.title} | {self.ip}'
