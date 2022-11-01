from django.urls import path, re_path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path("", views.index, name='index'),
    path("<str:page>/", views.other_page, name='other_page'),
    path("accounts/login/", views.BBLoginView.as_view(), name='login'),
    path("account/logout/", views.BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/change/', views.change_user_view, name='change_profile'),
    path('accounts/password/change/', views.change_password, name='change_password'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', views.register_done, name='register_done'),
    path('accounts/delete/<int:pk>', views.BBDeleteView.as_view(), name='delete'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('password/reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
