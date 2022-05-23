import json
from .models import *

def cookiePanier(request):

	#Create empty panier for now for non-logged in user
	try:
		panier = json.loads(request.COOKIES['panier'])
	except:
		panier = {}
		print('PANIER:', panier)

	details = []
	commande = {'get_panier_total':0, 'get_panier_details':0, 'livraison':False}
	detailpaniers = commande['get_panier_details']

	for i in panier:
		#We use try block to prevent details in panier that may have been removed from causing error
		try:	
			if(panier[i]['quantite']>0): #details with negative quantite = lot of freebies  
				detailpaniers += panier[i]['quantite']

				produit = Produit.objects.get(id=i)
				total = (produit.prix * panier[i]['quantite'])

				commande['get_panier_total'] += total
				commande['get_panier_details'] += panier[i]['quantite']

				detail = {
				'id':produit.id,
				'produit':{'id':produit.id,'designation':produit.designation, 'prix':produit.prix, 
				'imageURL':produit.imageURL}, 'quantite':panier[i]['quantite'], 'get_total':total,
				}
				details.append(detail)

				commande['livraison'] = True
		except:
			pass
			
	return {'detailpaniers':detailpaniers ,'commande':commande, 'details':details}

def panierData(request):
	if request.user.is_authenticated:
		client = request.user.client
		commande, created = Commande.objects.get_or_create(client=client, complete=False)
		details = commande.commandedetail_set.all()
		detailpaniers = commande.get_panier_details
		produittotal = commande.get_produit_total
	else:
		cookieData = cookiePanier(request)
		detailpaniers = cookieData['detailpaniers']
		commande = cookieData['commande']
		details = cookieData['details']
		produittotal = 0

	return {'detailpaniers':detailpaniers ,'commande':commande, 'details':details, 'produittotal': produittotal}

	
def guestcommande(request, data):
	cookieData = cookiePanier(request)
	details = cookieData['details']

	client = request.user.client

	commande = Commande.objects.create(
		client=client,
		complete=False,
		)

	for detail in details:
		produit = Produit.objects.get(id=detail['id'])
		commandedetail = CommandeDetail.objects.create(
			produit=produit,
			commande=commande,
			quantite=(detail['quantite'] if detail['quantite']>0 else -1*detail['quantite']), # negative quantite = freebies
		)
	return client, commande

