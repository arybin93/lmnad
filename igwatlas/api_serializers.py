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


class FeatureRecordYandexSerialzer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ('id',
                  'type',
                  'geometry',
                  'properties'
                  )

    def get_type(self, obj):
        return 'Feature'

    def get_geometry(self, obj):
        lat = obj.position.latitude
        lon = obj.position.longitude
        return {
            'type': 'Point',
            'coordinates': [lat, lon]
        }

    def get_properties(self, obj):
        short_text_source = ''
        full_text_source = ''
        link_text_source = ''
        for source in obj.source.all():
            short_text_source += source.source_short + ';'
            full_text_source += source.source + ';'
            if source.link:
                link_text_source += source.link + ';'

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
            'hintContent': short_text_source + str(obj.position),
            'balloonContentHeader': obj.get_text_types(),
            'balloonContentBody': full_text_source + "<br>" + img + "<br>" + str(obj.position),
            'balloonContentFooter': link_text_source + ' ' + date,
            'clusterCaption': obj.get_text_types()
        }


class RecordYandexSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=200)
    features = FeatureRecordYandexSerialzer(many=True)


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

        date = ''
        if obj.record.date:
            date = obj.record.date.strftime('%d-%m-%Y')

        return {
            'hintContent': short_text_source + str(obj.record.position),
            # 'balloonContentHeader': str(obj.type) + ' ' + str(obj.mode) + ' ' + str(obj.amplitude),
            'balloonContentBody': full_text_source + "<br>" + str(obj.record.position) + "<br>",
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
                  'record'
                  )

    def get_lat(self, obj):
        return obj.record.position.latitude

    def get_lon(self, obj):
        return obj.record.position.longitude
