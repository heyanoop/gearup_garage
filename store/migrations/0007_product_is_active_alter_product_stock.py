# Generated by Django 5.0.3 on 2024-06-18 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_variation_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]