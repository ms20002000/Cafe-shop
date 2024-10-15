from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login, name='login'),
    # path('login_first/', login_first, name='login_first'),
    # path('logout/', logout, name='logout'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('register/', RegularUserCreateView.as_view(), name='rigister'),
    path('list_user/', RegularUserListView.as_view(), name='list_user'),
    
]