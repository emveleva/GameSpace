from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from accounts.views import RegisterView, DashboardView, UserLogoutView, EditProfileView, DeleteProfileView, \
    ProfileDetailsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile-details/', ProfileDetailsView.as_view(), name='profile-details'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),
]