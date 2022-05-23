from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from .decorators import *
import json
from .utils import *
# Create your views here.

@unauthentificated_user
def register(request):
    context ={}
    if request.POST:
        form=CreationUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            client = Client.objects.create(
                user=user,
            )
            Adresse.objects.create(
                client = client,
            )
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('info')
            #messages.success(request,'Création de compte réussi')
            return redirect('info')
        
        context = {'form': form}
    return render(request, "account/inscription.html", context)

@login_required(login_url='login')
def info(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    
    client = request.user.client
    info_form = ClientForm(instance=client)

    if request.method == 'POST':
        info_form = ClientForm(request.POST, instance = client)
        if info_form.is_valid():
            info_form.save()
        return redirect('adresse')

    context={'info_form': info_form,'produits':produits, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, 'account/register_info.html', context)

@login_required(login_url='login')
def adresse(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    adresse = request.user.client.adresse
    form = AddressForm(instance=adresse)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=adresse)
        if form.is_valid():
            form.save()

        return redirect('profil')
    context = {'form': form,'produits':produits, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, 'account/register_adresse.html', context)

@unauthentificated_user
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
           
        if user is not None:
            login(request, user)
            return redirect('index')
        #else:
            #messages.info(request, 'Username Or Password is incorrect')
            
    context = {}
    return render(request, "account/connexion.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profil(request):
    
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    
    client = request.user.client
    info_form = ClientForm(instance=client)

    if request.method == 'POST':
        info_form = ClientForm(request.POST, instance = client)
        if info_form.is_valid():
            info_form.save()
            

    adresse = request.user.client.adresse
    adresse_form = AddressForm(instance=adresse)

    if request.method == 'POST':
        adresse_form = AddressForm(request.POST, instance=adresse)
        if adresse_form.is_valid():
            adresse_form.save()
            #browswer.refresh()

    context={'info_form':info_form,'adresse_form':adresse_form,'produits':produits, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, 'account/account.html', context)


#@allowed_users(allowed_roles=['utilisateur'])
def index(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    context={'produits':produits, 'detailpaniers': detailpaniers,'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, "pages/index.html",context)

def boutique(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    context={'produits':produits, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, "pages/shop.html",context)

def detail(request,refProduit,id):
    
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.get(id=id)
    context={'produits':produits, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, "pages/detail.html", context)

@login_required(login_url='login')
def checkout(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    
    context = {'details': details, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, "pages/checkout.html", context)

@login_required(login_url='login')
def commande(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    

    context = {'details': details,'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, "pages/facture.html", context)


@login_required(login_url='login')
def panier(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()

    context = {'produits':produits,'details': details,'detailpaniers': detailpaniers, 'commande': commande, 'produittotal':produittotal}
    return render(request, "pages/cart.html", context)

@login_required(login_url='login')
def updateDetail(request):

    data = json.loads(request.body)
    produit_id = data['produit_id']
    action = data['action']

    client = request.user.client
    produit = Produit.objects.get(id=produit_id)
    commande , created = Commande.objects.get_or_create(client = client, complete = False)

    commandedetail, created = CommandeDetail.objects.get_or_create(commande = commande, produit = produit)

    if action == 'add':
        commandedetail.quantite = (commandedetail.quantite + 1)
    elif action =='remove':
        commandedetail.quantite = (commandedetail.quantite - 1)
    elif action =='retirer':
        commandedetail.quantite = 0
    
    commandedetail.save()

    if commandedetail.quantite <= 0:
        commandedetail.delete()

    return JsonResponse('Detail ajout', safe=False)

   

def propos(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    
    context={'produits':produits, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, "pages/about.html", context)

def contact(request):
    data = panierData(request)

    detailpaniers = data['detailpaniers']
    commande = data['commande']
    details = data['details']
    produittotal = data['produittotal']

    produits=Produit.objects.all()
    
    context={'produits':produits, 'detailpaniers': detailpaniers, 'commande': commande, 'details': details, 'produittotal':produittotal}
    return render(request, "pages/contact.html", context)

def  set_password(request):
    context={}
    return render(request, "account/set_password.html")
