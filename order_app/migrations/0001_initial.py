# Generated by Django 4.2.3 on 2023-08-20 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_app', '0003_ratingproduct_is_active_ratingproduct_is_delete_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_cart', 'در سبد خرید'), ('canceled', 'لغو شده'), ('pending_payment', ' در انتظار پرداخت'), ('paid', ' پرداخت شده')], max_length=20)),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='date of payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.IntegerField(blank=True, null=True, verbose_name='final_price')),
                ('count', models.IntegerField(verbose_name='count')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_app.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.product', verbose_name='product')),
            ],
        ),
    ]
