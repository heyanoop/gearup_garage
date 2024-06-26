# Generated by Django 5.0.3 on 2024-05-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_is_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('CONFIRMED', 'confirmed'), ('SHIPPED', 'shipped'), ('CANCELLED', 'cancelled'), ('RETURN', 'return')], default='PENDING', max_length=20),
        ),
    ]
