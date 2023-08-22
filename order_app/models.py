from django.db import models
from user_app.models import User, Profile
from product_app.models import Product


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
