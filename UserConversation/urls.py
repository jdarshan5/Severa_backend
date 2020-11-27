from django.urls import path

from UserConversation import views

urlpatterns = [
    path('sendMsg/', views.send_message)
]
