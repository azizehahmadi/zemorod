# Generated by Django 4.2.3 on 2023-08-21 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in_cart', 'در سبد خرید'), ('no_paid', 'پرداخت نشده'), ('canceled', 'لغو شده'), ('pending_payment', ' در انتظار پرداخت'), ('paid', ' پرداخت شده')], max_length=20),
        ),
    ]
