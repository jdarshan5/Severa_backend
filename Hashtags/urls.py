from django.urls import path

from . import views

urlpatterns = [
    path('hashtagCount/', views.get_hashtag_count)
]