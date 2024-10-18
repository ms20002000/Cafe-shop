# Generated by Django 5.1.2 on 2024-10-18 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_customuser_specialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='specialty',
            field=models.CharField(blank=True, choices=[('M', 'Manager'), ('Ca', 'Cashier'), ('B', 'Bartender'), ('Co', 'Cook'), ('W', 'Waiter'), ('Ws', 'Waitress')], max_length=100, null=True),
        ),
    ]