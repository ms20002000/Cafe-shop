from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page=reverse_lazy('list_user')), name='logout'),
    # path('login_first/', login_first, name='login_first'),
    # path('logout/', logout, name='logout'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('register/', RegularUserCreateView.as_view(), name='rigister'),
    path('list_user/', RegularUserListView.as_view(), name='list_user'),
    
]