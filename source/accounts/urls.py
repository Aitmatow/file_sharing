from django.urls import path
from accounts.views import login_view, logout_view, register_view, UserDetailView, \
    UserPersonalInfoChangeView, UsersList

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('users/', UsersList.as_view(),name='users_list'),
]

app_name = 'accounts'