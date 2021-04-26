"""djinn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter

from django.conf import settings
from main.views import CategoryListView, PostViewSet, PostImageView, CommentViewSet, LikeViewSet
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rating.views import ObjectRatingViewSet, RatingElementViewSet

router = DefaultRouter()
router.register('comment', CommentViewSet)
router.register('posts', PostViewSet)
router.register('likes', LikeViewSet)
router.register('objectratings', ObjectRatingViewSet)
router.register('ratingelements', RatingElementViewSet)



schema_view = get_schema_view(
   openapi.Info(
      title="projectDjinn API",
      default_version='v1',
      description="Djinn description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('v1/api/categories/', CategoryListView.as_view()),
    path('api/v1/categories/', include(router.urls)),
    path('api/v1/likes/', include('main.urls')),
    path('v1/api/add-image/', PostImageView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/', include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
