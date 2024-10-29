from typing import TYPE_CHECKING

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.fields import CharField, ImageField
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Image
from api.serializers import ImageSerializer
from api.tools.image import create_image

if TYPE_CHECKING:
    from django.core.files.uploadedfile import TemporaryUploadedFile
    from django.db.models import QuerySet
    from rest_framework.request import Request
    from rest_framework.serializers import Serializer


class ImageViewSet(ModelViewSet):
    queryset: 'QuerySet[Image]' = Image.objects.all()
    serializer_class: 'Serializer' = ImageSerializer

    @extend_schema(request=inline_serializer(name='Upload', fields={'resolution': CharField(), 'file': ImageField()}))
    @action(detail=False, methods=['POST'])
    def upload(self, request: 'Request') -> Response:
        # try:
        file: TemporaryUploadedFile = request.FILES['file']

        if file and 'image' in file.content_type:
            image: Image = create_image(file)
            return Response(image.name, status.HTTP_201_CREATED)
        raise APIException('Отправленный файл не является изображением')
        #
        # except Exception as exc:
        #     print(exc)
        #     return Response(exc, status.HTTP_500_INTERNAL_SERVER_ERROR)
