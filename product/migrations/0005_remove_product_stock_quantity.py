# Generated by Django 5.1.2 on 2024-11-04 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock_quantity',
        ),
    ]