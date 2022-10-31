from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("<str:page>/", views.other_page, name='other_page'),
    path("accounts/login/", views.BBLoginView.as_view(), name='login'),
    path("account/logout/", views.BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/change/', views.change_user_view, name='change_profile'),
    path('accounts/password/change/', views.change_password, name='change_password'),
    path('account/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', views.register_done, name='register_done'),
    path('account/delete/<int:pk>', views.BBDeleteView.as_view(), name='delete'),
]
