from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "users"

urlpatterns = [
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('add/', views.UserAddView.as_view(), name="add"),
    path('edit/<int:pk>', views.UserEditView.as_view(), name="edit"),
    path('delete/<int:pk>', views.UserDeleteView.as_view(), name="delete"),
    path('verify/', views.VerifyUser.as_view(), name='verify'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('logs/', views.LogsView.as_view(), name='logs'),
    path('', views.UsersView.as_view(), name='users')
]