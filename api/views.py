from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.fields import CharField, ImageField
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.consts import IMAGE_STORE_PATH
from api.models import Image
from api.serializers import ImageSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @extend_schema(request=inline_serializer(name='Upload', fields={'resolution': CharField(), 'file': ImageField()}))
    @action(detail=False, methods=['POST'])
    def upload(self, request: Request) -> Response:
        try:
            file = request.FILES['file']
            with open(f'{IMAGE_STORE_PATH}/' + file.name, 'wb+') as uploaded_file:
                for chunk in file.chunks():
                    uploaded_file.write(chunk)
            return Response(file.name, status.HTTP_201_CREATED)

        except Exception as exc:
            print(exc)
            return Response(exc, status.HTTP_500_INTERNAL_SERVER_ERROR)
