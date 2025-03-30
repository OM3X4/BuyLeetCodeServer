from django.urls import path

from .views import get_questions , get_posts , register , upVote , comments , get_companies , get_tags , get_question

urlpatterns = [
    # questions/?offset=x&limit=y
    path('questions/', get_questions),
    # Question/id/
    path("questions/<int:pk>/" , get_question),
    # posts/?offset=x&limit=y
    path('posts/' , get_posts),
    path("register/" , register),
    path("upvote/<int:pk>/" , upVote),
    path("comments/<int:pk>/" , comments),
    path("companies/" , get_companies),
    path("tags/" , get_tags),
]
