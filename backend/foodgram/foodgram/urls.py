from django.contrib import admin
from django.urls import re_path, path, include
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

from api.views import RecipesViewSet, IngredientsViewSet
from api.views import TagsViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipesViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
