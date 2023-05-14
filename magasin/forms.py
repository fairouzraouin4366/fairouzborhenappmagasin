from django import forms
from django.forms import ModelForm
from .models import Produit,Fournisseur,Categorie,Commande,Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProduitForm(ModelForm):
    class Meta :
        model = Produit
        fields = "__all__" #pour tous les champs de la table
        #fields=['libelle','description'] #pour qulques champs
class FournisseurForm(ModelForm):
    class Meta : 
        model = Fournisseur
        fields = "__all__" #pour tous les champs de la table

class ChangerMdpForm(forms.Form):
    email = forms.EmailField(label='Adresse email', max_length=100)

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = "__all__" 
class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = "__all__" 
        
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__" 

