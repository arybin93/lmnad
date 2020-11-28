from django.contrib import admin
from django.forms import ModelForm
from suit.widgets import SuitDateWidget

from igwatlas.admin import RowDateRangeFilter
from .models import SeaPhenomenon


class RecordForm(ModelForm):
    class Meta:
        model = SeaPhenomenon
        exclude = []
        widgets = {
            'date': SuitDateWidget(),
            'date_start': SuitDateWidget(),
            'date_stop': SuitDateWidget()
        }


@admin.register(SeaPhenomenon)
class SeaPhenomenonAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'type_phenomenon',
                    'name',
                    'place',
                    'get_position',
                    'date',
                    'date_start',
                    'date_end',
                    'wind_speed',
                    'height_wave',
                    'source_link')
    list_display_links = ('id', 'type_phenomenon')
    list_filter = ['type_phenomenon', ('date', RowDateRangeFilter)]
    search_fields = ['name', 'place']
    form = RecordForm

    def get_position(self, obj):
        if obj.position:
            latitude = round(float(obj.position.latitude), 3)
            longitude = round(float(obj.position.longitude), 3)
            return '{lat}, {lon}'.format(lat=latitude, lon=longitude)
        return '-'
    get_position.short_description = 'Координаты (Широта, Долгота)'
