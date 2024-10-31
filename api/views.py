from typing import TYPE_CHECKING, Type

from django.core.cache import cache
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Image
from api.serializers import ImageRead, ImageWrite
from api.tasks import process_image_task, run_task
from project.rabbitmq import produce_message

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.serializers import Serializer


class ImageViewSet(ModelViewSet):
    queryset: 'QuerySet[Image]' = Image.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Type['Serializer']:
        if self.action in ('create', 'update', 'partial_update'):
            return ImageWrite
        return ImageRead

    def retrieve(self, request: Request, *args: list, **kwargs: dict) -> Response:
        pk = kwargs.get('pk')
        cache_key = f'image_detail_{pk}'

        if data := cache.get(cache_key):
            return Response(data)

        response = super().retrieve(request, pk=pk)
        cache.set(cache_key, response.data)
        return response

    def perform_create(self, serializer: 'Serializer') -> None:
        serializer.is_valid(raise_exception=True)
        image = serializer.save(size=self.request.FILES['file'].size)
        produce_message(f'{image.upload_dt} создано изображение "{image.name}" ({image.file.path})')

        run_task(process_image_task, image)

    def perform_update(self, serializer: 'Serializer') -> None:
        super().perform_update(serializer)
        image = self.get_object()
        produce_message(f'Изображение "{image.name}" ({image.file.path}) было обновлено {now()}')

        if serializer.validated_data.get('file'):
            run_task(process_image_task, image)

    def perform_destroy(self, instance: Image) -> None:
        produce_message(f'Изображение "{instance.name}" ({instance.file.path}) было удалено {now()}')
        super().perform_destroy(instance)
