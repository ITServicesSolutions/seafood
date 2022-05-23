from django.urls import path
from .views import * 

urlpatterns = [
    path('', index, name="index"),
    path('register/', register, name="register"),
    path('info/', info, name="info"),
    path('adresse/', adresse, name="adresse"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('profil/', profil, name="profil"),
    path('boutique/', boutique, name="boutique"),
    path('propos/', propos, name="propos"),
    path('contact/', contact, name="contact"),
    path('panier/', panier, name="panier"),
    path('detail/<str:refProduit>/<int:id>',detail, name="detail"),
    path('checkout/',checkout, name="checkout"),
    path('commande/',commande, name="commande"),
    path('set_password/',set_password, name="set_password"),
    path('update_detail/',updateDetail, name="update_detail"),
]
