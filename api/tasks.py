from typing import Any, Callable

from django.conf import settings

from api.models import Image
from api.tools.image import process_image
from project.celery import app


def run_task(task: Callable, *args: list, **kwargs: dict) -> Any:  # noqa
    """Функция общего назначения для запуска Celery задач"""
    delay_time = kwargs.pop('delay_time', None)
    if settings.DEBUG:
        # выполнение задачи без celery
        return task(*args, **kwargs)

    return task.apply_async(eta=delay_time, args=args, kwargs=kwargs)


@app.task
def process_image_task(image: Image) -> None:
    """Celery задача для обработки изображений"""
    process_image(image)
