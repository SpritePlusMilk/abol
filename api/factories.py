from datetime import datetime

import factory
from django.contrib.auth.models import User
from factory import fuzzy
from faker import Factory

from api.consts import RESOLUTION_CHOICES
from api.models import Image

factory_ru = Factory.create(locale='ru_Ru')


class User(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: factory_ru.user_name())
    email = factory.Sequence(lambda n: factory_ru.email())
    first_name = factory.Sequence(lambda n: factory_ru.first_name())
    last_name = factory.Sequence(lambda n: factory_ru.last_name())
    password = factory.Sequence(lambda n: factory_ru.word())

    class Meta:
        model = User


class Image(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: factory_ru.word())
    file = factory.django.FileField()
    upload_dt = fuzzy.FuzzyDate(datetime(2024, 1, 1), datetime(2024, 12, 31))
    resolution = fuzzy.FuzzyChoice(i[0] for i in RESOLUTION_CHOICES)
    size = fuzzy.FuzzyInteger(1, 1000)

    class Meta:
        model = Image
