from rest_framework import serializers

from api.models import Image


class ImageRead(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ImageWrite(serializers.ModelSerializer):
    resolution = serializers.CharField(required=False)

    class Meta:
        model = Image
        fields = ('name', 'file', 'resolution')
