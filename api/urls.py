from rest_framework.routers import DefaultRouter

from api.views import ImageViewSet

app_name = 'api'

router = DefaultRouter()
router.register('images', ImageViewSet, 'images')

urlpatterns = router.urls
