from django.urls import path
from.import views

urlpatterns = [
    path('register/', views.user_registration, name='user_registration'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('create/', views.create_content, name='create_content'),
    path('edit/<int:content_id>/', views.edit_content, name='edit_content'),
    path('delete/<int:content_id>/', views.delete_content, name='delete_content'),
    path('search/', views.search_content, name='search_content'),
    path('view/<int:content_id>/', views.view_content, name='view_content'),
]
