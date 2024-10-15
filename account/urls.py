from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('register/', RegularUserCreateView.as_view(), name='register'),
    path('list_user/', RegularUserListView.as_view(), name='list_user'),
]