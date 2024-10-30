from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('create_record/', views.create_record, name='create_record'),
    path('record_detail/<int:record_id>/', views.record_detail, name='record_detail'),
    path('update_record/<int:record_id>/', views.update_record, name='update_record'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('search_record/', views.search, name='search'),

    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.log_out, name='logout'),
]