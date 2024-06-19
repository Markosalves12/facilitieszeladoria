from django.contrib import admin
from materiais.models import Materiais

# Register your models here.
class MateriaisAdmin(admin.ModelAdmin):
    list_display = ('material', 'categoria', 'consumo', )

admin.site.register(Materiais, MateriaisAdmin)