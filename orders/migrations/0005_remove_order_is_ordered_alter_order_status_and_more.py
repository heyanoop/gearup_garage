# Generated by Django 5.0.3 on 2024-05-09 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_orderproduct_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_ordered',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('CONFIRMED', 'confirmed'), ('SHIPPED', 'shipped'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='ordered',
            field=models.BooleanField(default=True),
        ),
    ]