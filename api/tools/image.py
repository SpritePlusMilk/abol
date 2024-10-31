from PIL import Image

from api.models import Image as Image_


def get_size(resolution: str) -> tuple[int, int]:
    x_position = resolution.find('x')
    width = int(resolution[:x_position])
    height = int(resolution[x_position + 1 :])

    return width, height


def process_image(image: Image_) -> None:
    with Image.open(image.file.path) as processed_image:
        processed_image.convert('L')
        processed_image.thumbnail((get_size(image.resolution)), Image.Resampling.BOX)
        processed_image.save(image.file.path)
