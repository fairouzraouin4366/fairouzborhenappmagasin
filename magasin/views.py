from .models import Produit, Fournisseur,Contact,Categorie,Commande
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from .forms import ProduitForm, FournisseurForm
from django.shortcuts import redirect,render ,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import permission_required,login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from magasin.models import Categorie,Produit,Product
from magasin.serializers import CategorySerializer,ProduitSerializer
from .forms import ChangerMdpForm,CategorieForm,CommandeForm


@permission_required('magasin.majProduits.html')
def manipprod(request):
       if request.method == "POST" :
         form = ProduitForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              list=Produit.objects.all()
              return render(request,'magasin/vitrine.html',{'list':list})
       else : 
            form = ProduitForm() #créer formulaire vide 
            list=Produit.objects.all()
            return render(request,'magasin/majProduits.html',{'form':form,'list':list})

def Catalogue(request):	
	products= Produit.objects.all()
	context={'products':products}
	return render(request,'magasin/mesProduits.html',context )
def listprod(request):
	list=Produit.objects.all()
	return render(request,'magasin/vitrine.html',{'list':list})	
@permission_required('magasin.modifierProduit.html')
def modifierProduit(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            produit = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['img']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                produit.img = nouvelle_image
            # Sauvegarder le produit
            produit.save()
            return redirect('Catalogue')
    else:
        form = ProduitForm(instance=product)
    return render(request, 'magasin/modifierProduit.html', {'form': form})
@permission_required('magasin/effacerProduit.html')
def effacerProduit(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('Catalogue')
    return render(request, 'magasin/effacerProduit.html', {'product': product})
def detailProduit(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    context = {'produit': produit}
    return render(request, 'magasin/detailProduit.html', context)

#fournisseurs

@permission_required('magasin.fournisseur.html')
def nouveauFournisseur(request):
    if request.method == "POST" :
         form = FournisseurForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              nouvFournisseur=Fournisseur.objects.all()
              return render(request,'magasin/vitrineF.html',{'nouvFournisseur':nouvFournisseur})
    else : 
            form = FournisseurForm() #créer formulaire vide 
            nouvFournisseur=Fournisseur.objects.all()
            return render(request,'magasin/fournisseur.html',{'form':form,'nouvFournisseur':nouvFournisseur})
@permission_required('magasin/fournisseur.html')
def fournisseur(request):
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'magasin/mesFournisseurs.html', context)




def modifier_fournisseur(request, id):
          fournisseur = Fournisseur.objects.get( id=id)
          if request.method == 'POST':
             form = FournisseurForm(request.POST, request.FILES, instance=fournisseur)
             if form.is_valid():
                form.save()
                return redirect('fournisseurs')
          else:
             form = FournisseurForm(instance=fournisseur)
          return render(request, 'magasin/edit_fournisseur.html',{'form': form})

def supprimer_fournisseur(request, id):
     fournisseur = Fournisseur.objects.get( id=id)
     if request.method == 'POST':
        fournisseur.delete()
        return redirect('fournisseurs')
     return render(request, 'magasin/delete_fournisseur.html', {'fournisseur': fournisseur})
     

#comptes

def register(request):
     if request.method == 'POST' :
          form = UserCreationForm(request.POST)
          if form.is_valid():
               form.save()
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password1')
               user = authenticate(username=username, password=password)
               login(request,user)
               messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
               return redirect('index')
     else :
          form = UserCreationForm()
     return render(request,'registration/register.html',{'form' : form})

#api

class CategoryAPIView(APIView):
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
class ProduitAPIView(APIView):
    def get(self, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)
class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer
    def get_queryset(self):
        queryset = Produit.objects.filter()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset

#accueil
def index(request):
  return render(request,'magasin/accueil.html' )
 
#contact
def contact(request):
    if request.method=='POST':
        print(request.POST)
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name,email,phone,content)
        if len(name)<1 or len(email)<3 or len(phone)<5 or len(content)==0:
            messages.error(request,'remplissez tout les champs !')

        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'Votre message est envoyé avec succes')

    return render(request,'magasin/contact.html')


def changer_mdp(request):
    form = ChangerMdpForm()
    return render(request, 'registration/changer_mdp.html', {'form': form})

#categories

@login_required
def categories(request):
        categories= Categorie.objects.all()
        context={'categories':categories}
        return render( request,'magasin/mescategories.html',context )
@permission_required('magasin.ajoutcategorie.html')
def ajoutercategorie(request):
    if request.method == "POST":
        form = CategorieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            categories = Categorie.objects.all()
            return render(request, 'magasin/mescategories.html', {'categories': categories})
        else: 
            categories = Categorie.objects.all()
            return render(request, 'magasin/ajoutcategorie.html', {'form': form, 'categories': categories})
    else:
        form = CategorieForm()
        categories = Categorie.objects.all()
        return render(request, 'magasin/ajoutcategorie.html', {'form': form, 'categories': categories})

#commandes
@permission_required('magasin/mescommandes.html')
def ListCommande(request):
    commandes= Commande.objects.all()
    context={'commandes':commandes}
    return render( request,'magasin/mescommandes.html',context )
@permission_required('magasin/delete_commande.html')
def delete_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('ListCommande')
    return render(request, 'magasin/delete_commande.html', {'commande': commande})
@permission_required('magasin//detail_commande.html')
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    context = {'commande': commande}
    return render(request, 'magasin/detail_commande.html', context)
@permission_required('magasin//edit_commande.html')
def edit_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('ListCommande')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'magasin/edit_commande.html', {'form': form})




from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)
@login_required
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)
@login_required
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

