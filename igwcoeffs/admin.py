from django.contrib import admin

# Register your models here.
from igwcoeffs.models import Calculation


class CalculationAdmin(admin.ModelAdmin):
    list_display = ['name', 'types', 'mode', 'created']
    exclude = ['parse_file_fields', 'parse_start_from', 'parse_separator']
    search_fields = ['name']
    list_filter = ['types', 'mode']
    readonly_fields = ['types', 'mode', 'email']

    def has_add_permission(self, request):
        return False

admin.site.register(Calculation, CalculationAdmin)
