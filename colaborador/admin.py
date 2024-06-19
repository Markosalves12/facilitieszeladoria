from django.contrib import admin
from colaborador.models import Colaborador

# Register your models here.
class Colaboradordmin(admin.ModelAdmin):
    # Não foi possivel inserir a coluna de gerentes por ser do tipo ManyToManyField
    list_display = ("id", "nome", "email", "funcao", "status", )
    list_display_links = ("id", "nome", "email", "status", )
    search_fields = ("nome", "status", )
    list_filter = ("status", )

    list_per_page = 20

##########################################

## Classe administrador removida temporariamente do sistema por mudança na estratégia de gestão

# class Administradordmin(admin.ModelAdmin):
#     list_display = ("id", "nome", "email", "senha", "status", )
#     list_display_links = ("id", "nome", "email", "senha", "status", )
#     search_fields = ("nome",)
#     list_filter = ("nome",)
#
#     list_per_page = 20
#
#
# admin.site.register(Adminsitrador, Administradordmin)

###########################################

admin.site.register(Colaborador, Colaboradordmin)