from django.urls import path

from .views import get_questions , get_posts , register , upVote , comments , get_companies , get_tags , get_question , new_post
from .dataImportView import import_data


urlpatterns = [
    # questions/?offset=x&limit=y
    path('questions/', get_questions),
    # Question/id/
    path("questions/<int:pk>/" , get_question),
    # posts/?offset=x&limit=y
    path('posts/' , get_posts),
    path("newpost/" , new_post),
    path("register/" , register),
    path("upvote/<int:pk>/" , upVote),
    path("comments/<int:pk>/" , comments),
    path("companies/" , get_companies),
    path("tags/" , get_tags),
    path("import/" , import_data),

]
