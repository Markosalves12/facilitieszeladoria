from django.contrib import admin
from gestor.models import Gestor

class GestorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "funcao", "senha", "empresa", )
    list_display_links = ("id", "nome", "email", )
    search_fields = ("nome", )
    list_filter = ("nome", )

    list_per_page = 20

admin.site.register(Gestor, GestorAdmin)