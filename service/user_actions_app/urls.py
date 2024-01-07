from django.urls import path

from .views import QuestionViewSet, ReviewViewSet, AnswerViewSet


urlpatterns = [
    # Questions
    path('products/<int:product_pk>/questions/', QuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:product_pk>/questions/<int:pk>/', QuestionViewSet.as_view({
        'get': 'retrieve', 'patch': 'partial_update',
        'put': 'update', 'delete': 'destroy'
    })),

    # Reviews
    path('products/<int:product_pk>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:product_pk>/reviews/<int:pk>/', ReviewViewSet.as_view({
        'get': 'retrieve', 'patch': 'partial_update',
        'put': 'update', 'delete': 'destroy'
    })),

    # Answers for reviews and questions
    path('products/<int:product_pk>/reviews/<int:review_pk>/answers/', AnswerViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('products/<int:product_pk>/reviews/<int:review_pk>/answers/<int:pk>/', AnswerViewSet.as_view({
        'get': 'retrieve', 'patch': 'partial_update',
        'put': 'update', 'delete': 'destroy'
    })),

    path('products/<int:product_pk>/questions/<int:question_pk>/answers/', AnswerViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('products/<int:product_pk>/questions/<int:question_pk>/answers/<int:pk>/', AnswerViewSet.as_view({
        'get': 'retrieve', 'patch': 'partial_update',
        'put': 'update', 'delete': 'destroy'
    })),
]
