# Generated by Django 4.2 on 2023-05-13 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0012_remove_order_customer_remove_orderitem_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='adresse_livraison',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='commande',
            name='nom_client',
            field=models.CharField(default='', max_length=100),
        ),
    ]
