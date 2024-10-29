import os
from typing import TYPE_CHECKING

from PIL import Image

from api.consts import IMAGE_STORE_PATH, RESOLUTION_MEDIUM
from api.models import Image as Image_

if TYPE_CHECKING:
    from django.core.files.uploadedfile import TemporaryUploadedFile


def get_size(resolution: str) -> tuple[int, int]:
    x_position = resolution.find('x')
    width = int(resolution[:x_position])
    height = int(resolution[x_position + 1 :])

    return width, height


def process_image(file: 'TemporaryUploadedFile', resolution: str = RESOLUTION_MEDIUM) -> Image:
    file_name, extension = os.path.splitext(file.name)
    same_name_count = Image_.objects.filter(name__startswith=file_name, name__endswith=extension).count()
    image_name = f'{file_name} ({same_name_count}){extension}' if same_name_count else file.name
    image_path = IMAGE_STORE_PATH + image_name

    with open(image_path, 'wb+') as uploaded_image:
        for chunk in file.chunks():
            uploaded_image.write(chunk)

    with Image.open(image_path) as image:
        image.convert('L')
        image.thumbnail((get_size(resolution)), Image.Resampling.BOX)
        image.save(image_path)

    return Image_.objects.create(name=image_name, file=image_path, resolution=resolution, size=file.size)
