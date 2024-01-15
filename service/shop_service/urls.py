from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = [
    # admin panel
    path('admin/', admin.site.urls),

    # user app
    path('api/v1/', include('user_app.urls')),
    # authorization
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),

    # user actions app
    path('api/v1/', include('user_actions_app.urls')),

    # product app
    path('api/v1/', include('product_app.urls')),

    # cart app
    path('api/v1/', include('shopping_cart_app.urls')),

    # user app
    path('api/v1/', include('vendor_app.urls')),

    path("__debug__/", include("debug_toolbar.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
