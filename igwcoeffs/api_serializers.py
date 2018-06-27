from rest_framework import serializers


class CommonSerializer(serializers.Serializer):
    """ CommonSerializer """
    success = serializers.BooleanField(default=False, help_text="True if worked as planned")
    message = serializers.CharField(default=False, help_text="Message")
    reason = serializers.CharField(default=False, help_text="Reason if success false")
