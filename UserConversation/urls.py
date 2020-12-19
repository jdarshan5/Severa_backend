from django.urls import path

from UserConversation import views

urlpatterns = [
    path('sendMessage/', views.send_message),
    path('listOfMyConversation/', views.get_list_of_conversation),
    path('deleteMessage/', views.delete_a_message),
    path('conversationMessages/', views.get_messages_between_two_user),
    path('messageReceived/', views.message_received),
    path('messageRead/', views.message_read),
]
