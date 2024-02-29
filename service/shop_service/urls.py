from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

api_prefix = 'api/v1/'

urlpatterns = [
    # admin panel
    path('admin/', admin.site.urls),

    # user app
    path(api_prefix, include('user_app.urls')),

    # fixing tokens
    path(api_prefix + 'auth/', include('token_app.urls')),

    # authorization
    path(api_prefix + 'auth/', include('djoser.urls')),
    path(api_prefix + 'auth/', include('djoser.urls.jwt')),

    # user actions app
    path(api_prefix, include('user_actions_app.urls')),

    # product app
    path(api_prefix, include('product_app.urls')),

    # cart app
    path(api_prefix, include('shopping_cart_app.urls')),

    # orders app
    path(api_prefix, include('orders_app.urls')),

    # user app
    path(api_prefix, include('vendor_app.urls')),

    path("__debug__/", include("debug_toolbar.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
