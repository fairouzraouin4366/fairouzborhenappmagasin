# Generated by Django 4.2 on 2023-05-13 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0009_customer_order_shippingaddress_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user',
            new_name='User',
        ),
    ]
