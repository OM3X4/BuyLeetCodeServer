from django.urls import path

from .views import get_questions , get_posts

urlpatterns = [
    # questions/?offset=x&limit=y
    path('questions/', get_questions),
    # posts/?offset=x&limit=y
    path('posts/' , get_posts)
]
