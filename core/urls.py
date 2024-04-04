from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns


from .schema import swagger_urlpatterns


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/v1/common/', include('apps.common.urls')),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/branches/', include('apps.branches.urls')),
    path('api/v1/foods/', include('apps.foods.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
)

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
