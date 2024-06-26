# Generated by Django 3.2.12 on 2024-05-27 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0002_alter_coupon_discount_alter_coupon_valid_from'),
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_used',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupon.coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='original_price',
            field=models.IntegerField(default=0),
        ),
    ]
