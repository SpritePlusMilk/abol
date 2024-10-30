import tempfile
from unittest.mock import MagicMock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api import factories, serializers
from api.models import Image

MEDIA_ROOT = tempfile.mkdtemp(dir='tests')


def create_image_data() -> dict:
    temp_object = factories.Image()
    data = dict(serializers.ImageRead(temp_object).data)
    Image.objects.get(id=data.pop('id')).delete()

    return data


class TestApi(APITestCase):
    def setUp(self) -> None:
        self.user = factories.User()

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.image = factories.Image()
        self.initial_image_count = Image.objects.count()

    def test_list(self) -> None:
        url = reverse('api:images-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.initial_image_count)

    def test_list_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail(self) -> None:
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.image.id)
        self.assertEqual(response.data['first_name'], self.image.first_name)
        self.assertEqual(response.data['phone'], self.image.phone)

    def test_detail_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('project.rabbitmq.produce_message')
    def test_create(self, produce_message: MagicMock) -> None:
        url = reverse('api:images-list')
        data = create_image_data()

        response = self.client.post(url, data, format='json')

        produce_message.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(Image.objects.count(), self.initial_image_count)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['resolution'], data['resolution'])
        self.assertEqual(response.data['size'], data['size'])

    def test_create_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-list')

        response = self.client.post(url, create_image_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('project.rabbitmq.produce_message')
    def test_update(self, produce_message: MagicMock) -> None:
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        data = create_image_data()

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['file'], data['file'])
        self.assertEqual(response.data['resolution'], data['resolution'])
        self.assertEqual(response.data['size'], data['size'])
        produce_message.assert_called_once()

    def test_update_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.put(url, create_image_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('project.rabbitmq.produce_message')
    def test_partial_update(self, produce_message: MagicMock) -> None:
        image_before_update = serializers.ImageRead(self.image).data
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})
        data = {
            'name': create_image_data()['name'],
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['file'], image_before_update['file'])
        self.assertEqual(response.data['upload_dt'], image_before_update['upload_dt'])
        self.assertEqual(response.data['resolution'], image_before_update['resolution'])
        self.assertEqual(response.data['size'], image_before_update['size'])
        produce_message.assert_called_once()

    def test_partial_update_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.patch(url, create_image_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('project.rabbitmq.produce_message')
    def test_delete(self, produce_message: MagicMock) -> None:
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(Image.objects.count(), self.initial_image_count)
        produce_message.assert_called_once()

    def test_delete_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:images-detail', kwargs={'pk': self.image.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Image.objects.count(), self.initial_image_count)
