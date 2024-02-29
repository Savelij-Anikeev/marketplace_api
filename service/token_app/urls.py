from django.urls import path

from .views import TokenCustomCreateView, TokenCustomDestroyView, TokenCustomRefreshView

urlpatterns = [
    path('jwt/create/', TokenCustomCreateView.as_view()),
    path('jwt/delete/', TokenCustomDestroyView.as_view()),
    # path('jwt/refresh/', TokenCustomRefreshView.as_view()),
]
