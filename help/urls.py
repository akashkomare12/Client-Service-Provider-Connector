from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('', views.home, name='home'),
    path('register-page/', views.register_page, name='register_page'),
    path('register/', views.register_client, name='register_client'),
    path('login-page/', views.login_page, name='login_page'),
    path('login/', views.login_client, name='login_client'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('update-profile/', views.update_client_profile, name='update_client_profile'),
    path('update_client_page/', views.update_client_page, name='update_client_page'),
    path('client_service_page/', views.client_service_page, name='client_service_page'),
    path('logout/', views.logout_client, name='logout_client'),
    path('service-register-page/', views.service_register_page, name='service_register_page'),
    path('register_service_provider/', views.register_service_provider, name='register_service_provider'),
    path('service-login-page/', views.service_login_page, name='service_login_page'),
    path('login_service_provider/', views.login_service_provider, name='login_service_provider'),
    path('service_dashboard/', views.service_dashboard, name='service_dashboard'),
    path('service-update-profile/', views.update_service_provider, name='update_service_provider'),
    path('update_service_provider_page/', views.update_service_provider_page, name='update_service_provider_page'),
    path('logout_service_provide/', views.logout_service_provider, name='logout_service_provider'),
    # Service-related routes
    path('service_providers/', views.get_service_providers, name='get_service_providers'),
    path('book_service/', views.book_service, name='book_service'),
    path('get-service-records/', views.get_service_records, name='get_service_records'),
    path('edit_service_page/', views.edit_service_page, name='edit_service_page'),
    path('edit_service_record/<int:record_id>/', views.edit_service_record, name='edit_service_record'),
]
