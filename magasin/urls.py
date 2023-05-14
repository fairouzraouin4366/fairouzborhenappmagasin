from django.urls import path,include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CategoryAPIView,ProduitAPIView,ProductViewset
urlpatterns = [ 
    path('',views.index, name='index'),
    path('nouvFournisseur/',views.nouveauFournisseur,name='nouvFournisseur'),
    path('Catalogue/', views.Catalogue, name='Catalogue'),
    path('fournisseurs/', views.fournisseur, name='fournisseurs'),
    path('supprimer_fournisseur/<int:id>/',views. supprimer_fournisseur, name='supprimer_fournisseur'),  
    path('modifier_fournisseur/<int:id>/',views. modifier_fournisseur, name='modifier_fournisseur'),
    path('products/', views.manipprod, name='manipprod'),
    path('modifier/<int:pk>/', views.modifierProduit, name='modifierProduit'),
    path('effacer/<int:pk>/', views.effacerProduit, name='effacerProduit'),
    path('detail/<int:product_id>/', views.detailProduit, name='detailProduit'),
    path('register/',views.register, name = 'register'), 
    path('api-auth/', include('rest_framework.urls')),
    path('api/category/', CategoryAPIView.as_view()),
    path('api/produits/', ProduitAPIView.as_view()),
    path('contact/',views.contact,name='contact'),
    path('changer_mdp/', views.changer_mdp, name='changer_mdp'),
    path('categories/', views.categories, name='categories'),
    path('ajoutcategorie/', views.ajoutercategorie, name='ajoutercategorie'),
    path('commandes/', views.ListCommande, name='ListCommande'),
    path('editCommande/<int:pk>/', views.edit_commande, name='edit_commande'),
    path('deleteCommande/<int:pk>/', views.delete_commande, name='delete_commande'),
    path('Commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),
    path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
