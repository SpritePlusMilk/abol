from django.db import models

from api import consts


class Image(models.Model):
    name = models.CharField('Название', max_length=255)
    file = models.ImageField('Файл', upload_to=consts.IMAGE_STORE_PATH)
    upload_dt = models.DateTimeField('Дата и время загрузки', auto_now_add=True)
    resolution = models.CharField(
        'Разрешение', max_length=20, choices=consts.RESOLUTION_CHOICES, default=consts.RESOLUTION_MEDIUM
    )
    size = models.IntegerField('Размер', help_text='в байтах')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self) -> str:
        return f'{self.name[:15]}, {self.upload_dt} ({self.resolution})'
