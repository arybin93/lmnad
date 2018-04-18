from django.contrib import admin

# Register your models here.
from igwcoeffs.models import Calculation


class CalculationAdmin(admin.ModelAdmin):
    list_display = ['name', 'types', 'mode', 'created']

admin.site.register(Calculation, CalculationAdmin)
