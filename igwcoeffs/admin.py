from django.contrib import admin

# Register your models here.
from igwcoeffs.models import Calculation


class CalculationAdmin(admin.ModelAdmin):
    list_display = ['name', 'types', 'mode', 'created']
    exclude = ['parse_file_fields']
    search_fields = ['name']
    list_filter = ['types', 'mode']

    def has_add_permission(self, request):
        return False

admin.site.register(Calculation, CalculationAdmin)
