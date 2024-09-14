from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('check_email/', views.check_email, name='check_email'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'), 
    path('authenticate_email/', views.authenticate_email, name='authenticate_email'),  
    path('dashboard/', views.dashboard, name='dashboard'),   
    path('insert_database/', views.insert_database, name='insert_database'),
    path('delete/<int:pk>/', views.delete_registration, name='delete_registration'),
    path('update/<int:pk>/', views.update_registration, name='update_registration'),
]
