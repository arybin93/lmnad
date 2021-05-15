import random
from rest_framework import serializers
from igwatlas.models import Record, Source, File, RecordType, WaveData


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'source_short',
            'source',
            'link'
        )


class RecordTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordType
        fields = ('id', 'value', 'name')


class FeatureRecordYandexSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        fields = ('id',
                  'type',
                  'geometry',
                  'properties',
                  )

    def get_type(self, obj):
        return 'Feature'

    def get_geometry(self, obj):
        lat = float(obj.position.latitude) + random.uniform(0, 0.03)
        lon = float(obj.position.longitude) + random.uniform(0, 0.03)
        return {
            'type': 'Point',
            'coordinates': [lat, lon]
        }

    def get_properties(self, obj):
        return {
            'hintContent': str(obj.position),
        }


class RecordYandexSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=200, read_only=True)
    features = FeatureRecordYandexSerializer(many=True, read_only=True)


class FeatureRecordLabelsYandexSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'type',
            'geometry',
            'properties',
            'options',
        )

    def get_type(self, obj):
        return 'Feature'

    def get_geometry(self, obj):
        lat = float(obj.position.latitude) + random.uniform(0, 0.03)
        lon = float(obj.position.longitude) + random.uniform(0, 0.03)
        return {
            'type': 'Point',
            'coordinates': [lat, lon]
        }

    def get_properties(self, obj):
        return {
            'hintContent': str(obj.position),
            'iconContent': obj.get_first_type_label()
        }

    def get_options(self, obj):
        return {
            'preset': obj.get_first_type_color(),
        }


class RecordYandexLabelsSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=200, read_only=True)
    features = FeatureRecordLabelsYandexSerializer(many=True, read_only=True)


class YandexBalloonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    properties = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'properties'
        )

    def get_properties(self, obj):
        date = ''
        if obj.date:
            date = obj.date.strftime('%d-%m-%Y')

        img = ''
        if obj.image:
            img = (
                '<a target="_blank" href="{}">'
                '<img src="{}" style="height: 50px;" /></a><br/> '.format(
                    obj.image.url,
                    obj.image.url
                )
            )

        return {
            'hintContent': str(obj.position),
            'balloonContentHeader': obj.get_text_types(),
            'balloonContentBody': obj.get_sources() + "<br>" + img + "<br>" + str(obj.position),
            'balloonContentFooter': date,
            'clusterCaption': obj.get_text_types()
        }


class RecordSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()
    new_types = RecordTypeSerializer(many=True)
    source = SourceSerializer(many=True)

    class Meta:
        model = Record
        fields = ('id',
                  'lat',
                  'lon',
                  'new_types',
                  'date',
                  'date_start',
                  'date_stop',
                  'image',
                  'source',
                  'page'
                  )

    def get_lat(self, obj):
        return obj.position.latitude

    def get_lon(self, obj):
        return obj.position.longitude


class FeatureWaveDataYandexSerialzer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = WaveData
        fields = ('id',
                  'type',
                  'geometry',
                  'properties'
                  )

    def get_type(self, obj):
        return 'Feature'

    def get_geometry(self, obj):
        lat = obj.record.position.latitude
        lon = obj.record.position.longitude
        return {
            'type': 'Point',
            'coordinates': [lat, lon]
        }

    def get_properties(self, obj):
        short_text_source = ''
        full_text_source = ''
        link_text_source = ''
        for source in obj.record.source.all():
            short_text_source += source.source_short + ';'
            full_text_source += source.source + ';'
            if source.link:
                link_text_source += source.link + ';'

        period_str = str(obj.period) if obj.period else '-'
        polarity_str = obj.get_polarity_display() if obj.polarity else '-'

        date = ''
        if obj.record.date:
            date = obj.record.date.strftime('%d-%m-%Y')

        round_lat = round(obj.record.position.latitude, 3)
        round_lon = round(obj.record.position.longitude, 3)

        return {
            'hintContent': str(round_lat) + ',' + str(round_lon),
            'balloonContentHeader': "<b>" 'Тип ВГВ: ' + obj.get_type_display() + "<br>" +
                                    "<b>" 'Мода ВГВ: ' + str(obj.mode) + "<br>" + "<b>" 'Амплитуда ВГВ: ' +
                                    str(obj.amplitude) + ' м' + "<br>" + "<b>" 'Период ВГВ: ' +
                                    period_str + ' ч' "<br>" + "<b>" 'Полярность ВГВ: ' +
                                    polarity_str,
            'balloonContentBody': full_text_source + "<br>" + "<br>" + "<b>" 'Координаты: ' + str(round_lat) + ',' +
                                  str(round_lon) + "<br>",
            'balloonContentFooter': link_text_source + ' ' + date

        }


class WaveDataYandexSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=200)
    features = FeatureWaveDataYandexSerialzer(many=True)


class WaveDataSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()

    class Meta:
        model = WaveData
        fields = ('id',
                  'lat',
                  'lon',
                  'type',
                  'mode',
                  'amplitude',
                  'period',
                  'polarity',
                  'record'
                  )

    def get_lat(self, obj):
        return obj.record.position.latitude

    def get_lon(self, obj):
        return obj.record.position.longitude
