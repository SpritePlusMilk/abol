# Generated by Django 5.1.2 on 2024-10-29 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('file', models.ImageField(upload_to='images/', verbose_name='Файл')),
                ('upload_dt', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время загрузки')),
                ('resolution', models.CharField(choices=[('100x100', 'Маленькое'), ('500x500', 'Среднее'), ('900x900', 'Большое')], default='500x500', max_length=20, verbose_name='Разрешение')),
                ('size', models.IntegerField(help_text='в байтах', verbose_name='Размер')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]
