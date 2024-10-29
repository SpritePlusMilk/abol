from typing import TYPE_CHECKING, Type

from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models import Image
from api.serializers import ImageRead, ImageWrite
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

    def perform_create(self, serializer: 'Serializer') -> None:
        serializer.is_valid(raise_exception=True)
        image = serializer.save(size=self.request.FILES['file'].size)
        # process_image(image)
        produce_message(f'{image.upload_dt} создано изображение "{image.name}" ({image.file.path})')

    def perform_update(self, serializer: 'Serializer') -> None:
        super().perform_update(serializer)
        image = self.get_object()
        produce_message(f'Изображение "{image.name}" ({image.file.path}) было обновлено {now()}')

    def perform_destroy(self, instance: Image) -> None:
        produce_message(f'Изображение "{instance.name}" ({instance.file.path}) было удалено {now()}')
        super().perform_destroy(instance)
