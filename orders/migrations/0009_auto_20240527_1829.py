# Generated by Django 3.2.12 on 2024-05-27 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20240527_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='CASH ON DELIVERY', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default='PENDING', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
