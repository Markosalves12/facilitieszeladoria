from django.contrib import admin
from dashboards.models import FiltroTable

# Register your models here.
class FiltroTableAdmin(admin.ModelAdmin):
    list_display = ("id", "datastart", "datafim", )
    list_display_links = ("datastart", "datafim", )
    search_fields = ("datastart", "datafim", )

    list_per_page = 20

admin.site.register(FiltroTable, FiltroTableAdmin)