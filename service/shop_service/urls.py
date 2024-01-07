from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # admin panel
    path('admin/', admin.site.urls),

    # authorization
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),

    # user actions app
    path('api/v1/', include('user_actions_app.urls')),

    # product app
    path('api/v1/', include('product_app.urls')),

    # cart app
    path('api/v1/', include('shopping_cart_app.urls'))

]
