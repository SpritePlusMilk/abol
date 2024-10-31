from PIL import Image

from api.models import Image as Image_


def get_size(resolution: str) -> tuple[int, int]:
    """Функция для получения размеров, к которым приводится изображение при обработке"""
    x_position = resolution.find('x')
    width = int(resolution[:x_position])
    height = int(resolution[x_position + 1 :])

    return width, height


def turn_image_to_black_white(image_path: str) -> None:
    """Функция для перевода цветовой гаммы изображения в оттенки серого"""
    with Image.open(image_path) as processed_image:
        processed_image.convert('L')
        processed_image.save(image_path)


def resize_image(image_path: str, resolution: str) -> None:
    """Функция для изменения масштаба изображения"""
    with Image.open(image_path) as processed_image:
        processed_image.thumbnail((get_size(resolution)), Image.Resampling.BOX)
        processed_image.save(image_path)


def process_image(image: Image_) -> None:
    """Функция верхнего уровня для обработки загружаемого изображения"""
    turn_image_to_black_white(image.file.path)
    resize_image(image.file.path, image.resolution)
