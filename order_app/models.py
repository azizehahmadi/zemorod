from django.db import models
from user_app.models import User, Profile
from product_app.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from user_app.models import Profile


class Order(models.Model):

    status_choice = [
        ('no_paid', 'پرداخت نشده'),
        ('canceled', 'لغو شده'),
        ('pending_payment', ' در انتظار پرداخت'),
        ('paid', ' پرداخت شده'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    status = models.CharField(max_length=20, choices=status_choice)
    payment_date = models.DateField(null=True, blank=True, verbose_name='date of payment')

    def __str__(self):
        return str(self.user)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='final_price')
    count = models.IntegerField(verbose_name='count')

    def __str__(self):
        return str(self.order)


class RegisterOrder(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    order_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    count = models.IntegerField(validators=[MinValueValidator(1)])
    color = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user_profile.user} | {self.user_profile.phone} | {self.user_profile.title}"

