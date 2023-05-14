from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from magasin.models import Categorie,Produit

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'name']
class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model= Produit
        fields = ['id', 'libellé','description','catégorie']
         