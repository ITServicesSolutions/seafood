from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    nom = models.CharField(verbose_name="Nom", max_length=50,  null = True)
    prenom = models.CharField(verbose_name="Prenom", max_length=50,  null = True)
    entreprise = models.CharField(verbose_name="Entreprise", max_length=50,  null = True)
    mobile = PhoneNumberField(verbose_name="Téléphone", null = True)

    def __str__(self):
        return str(self.user)

class Adresse(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    adresse = models.CharField(max_length=200, null = True)
    ville = models.CharField(max_length=200, null = True)
    quartier = models.CharField(max_length=200, null = True)
    code_postal = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.adresse

class Categorie(models.Model):
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.designation


class Produit(models.Model):
    refProduit = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d",null=True, blank=True)
    designation = models.CharField(max_length=50)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    prix = models.FloatField()
    
    def __str__(self):
        return self.refProduit

    def imageURL(self):
        try:
            url=self.image.url
        except:
            url= ''
        return url

class Commande(models.Model):
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    dateCommande  = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default = False)

    def __str__(self):
        return str(self.id)

    @property
    def livraison(self):
        livrer = False
        commandedetails = self.commandedetail_set.all()
        for i in commandedetails:
            livrer = True
        return livrer

    
    @property
    def get_panier_total(self):
        commandedetails = self.commandedetail_set.all()
        total = sum([detail.get_total for detail in commandedetails])
        return total
    @property
    def get_panier_details(self):
        commandedetails = self.commandedetail_set.all()
        total = sum([detail.quantite for detail in commandedetails])
        return total
    
    @property
    def get_produit_total(self):
        commandedetails = self.commandedetail_set.all()
        total = 0
        for detail in commandedetails:
            total = total + 1
        return total

    

class CommandeDetail(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    date_ajout = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_total(self):
        total = self.produit.prix * float(self.quantite)
        return total

class Livraison(models.Model):
    client = models.ForeignKey(Client, verbose_name="Client", on_delete=models.SET_NULL, null=True)
    commande = models.ForeignKey(Commande, verbose_name="Commande", on_delete=models.SET_NULL, null=True)
    date_livrer = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.client)
    

class Commentaire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    commentaire = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.Client


class Fournisseur(models.Model):
    nom = models.CharField(max_length=50)
    prenom =models.CharField(max_length=50)
    nom_societe= models.CharField(max_length=80)
    adresse = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom_societe

class Approvisionnement(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantiteProduit = models.IntegerField()
    dateApprovisionnement = models.DateTimeField()
    prixApprovisionnement = models.FloatField()

    def __str__(self):
        return self.fournisseur 

   
class Balance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    solde = models.FloatField()

    def __str__(self):
        return self.Client

class Parametre(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reduction = models.FloatField()

    def __str__(self):
        return self.Client
    
class Stock(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_actuelle = models.IntegerField()

    def __str__(self):
        return self.produit