from django.test.utils import override_settings
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api import factories, serializers
from api.models import Image

factory_ru = Factory.create(locale='ru_Ru')


def create_image_data(valid: bool = True) -> dict:
    temp_object = factories.Image()
    data = dict(serializers.ImageRead(temp_object).data)
    data['file'] = open('api/tests/test_image.png', 'rb') if valid else open('api/tests/test_file.dat', 'rb')  # noqa
    Image.objects.get(id=data.pop('id')).delete()

    return data


class TestApi(APITestCase):
    def setUp(self) -> None:
        self.password = factory_ru.password()
        self.user = factories.User()
        self.user.set_password(self.password)

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.image = factories.Image()
        self.initial_image_count = Image.objects.count()

    def test_list(self) -> None:
        url = reverse('api:images-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.initial_image_count)

    def test_list_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(DEBUG=True)
    def test_detail(self) -> None:
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.image.id)
        self.assertEqual(response.data['name'], self.image.name)

    def test_detail_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(DEBUG=True)
    def test_create(self) -> None:
        url = reverse('api:images-list')
        data = create_image_data()

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(Image.objects.count(), self.initial_image_count)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['resolution'], data['resolution'])

    def test_create_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-list')

        response = self.client.post(url, create_image_data())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(DEBUG=True)
    def test_create_invalid_file_type(self) -> None:
        url = reverse('api:images-list')
        data = create_image_data(valid=False)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(DEBUG=True)
    def test_update(self) -> None:
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        data = create_image_data()

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['resolution'], data['resolution'])

    def test_update_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.put(url, create_image_data())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(DEBUG=True)
    def test_partial_update(self) -> None:
        image_before_update = serializers.ImageRead(self.image).data
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        data = {
            'name': create_image_data()['name'],
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['resolution'], image_before_update['resolution'])

    def test_partial_update_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.patch(url, create_image_data())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(DEBUG=True)
    def test_delete(self) -> None:
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(Image.objects.count(), self.initial_image_count)

    def test_delete_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Image.objects.count(), self.initial_image_count)
