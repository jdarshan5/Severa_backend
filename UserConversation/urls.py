from django.urls import path

from UserConversation import views

urlpatterns = [
    path('sendMsg/', views.send_message),
    path('listOfMyConversation/', views.get_list_of_conversation),
    path('deleteMessage/', views.delete_a_message),
    path('conversationMessages/', views.get_messages_between_two_user),
]
