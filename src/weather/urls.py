from drf_yasg import openapi
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from weather_app.views import WeatherList, StatsList
# from weather_app.views import WeatherViewSet, StatsViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version='v1',
        description="Weather API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# router = DefaultRouter()
# router.register(r'weather', WeatherViewSet)
# router.register(r'weather/stats', StatsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v2/', include(router.urls)),
    path('api/weather/', WeatherList.as_view(), name='weather-list'),
    path('api/weather/stats/', StatsList.as_view(), name='stats-list'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
