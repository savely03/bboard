from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("<str:page>/", views.other_page, name='other_page'),
    path("accounts/login/", views.BBLoginView.as_view(), name='login'),
    path("account/logout/", views.BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('account/profile/change/', views.change_user_view, name='change_profile'),
]
