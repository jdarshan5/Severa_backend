from django.urls import path, include
from Account import views

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'Account'

"""
    registration_view - Register view to register a new user.
    obtain_auth_token - Login view to retrieve the token of an existing user.
"""
urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('changeUserid/', views.change_userid),
    path('changePassword/', views.change_password),
    path('changeName/', views.change_name),
    path('checkUserid/', views.check_userid),
    path('rest-auth/', include('rest_auth.urls')),
]
