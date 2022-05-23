from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class ClientAdmin(admin.ModelAdmin):
    list_display=('id','user','nom','prenom','entreprise','mobile')
    ordering=('user',)


class CategorieAdmin(admin.ModelAdmin):
    list_display=('id','designation')
    ordering=('designation',)

    
admin.site.register(Adresse)
admin.site.register(Client, ClientAdmin)
admin.site.register(Commande)
admin.site.register(CommandeDetail)
admin.site.register(Produit)
admin.site.register(Categorie,CategorieAdmin)

