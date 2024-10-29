from typing import TYPE_CHECKING, Type

from rest_framework.viewsets import ModelViewSet

from api.models import Image
from api.serializers import ImageRead, ImageWrite

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.serializers import Serializer


class ImageViewSet(ModelViewSet):
    queryset: 'QuerySet[Image]' = Image.objects.all()

    def get_serializer_class(self) -> Type['Serializer']:
        if self.action in ('create', 'update', 'partial_update'):
            return ImageWrite
        return ImageRead

    def perform_create(self, serializer: 'Serializer') -> None:
        serializer.is_valid(raise_exception=True)
        image = serializer.save(size=self.request.FILES['file'].size)
        # process_image(image)
