from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import api_views as views

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/search/<str:name>/', views.category_search, name='category_search'),
    path('categories/<int:pk>/topics/', views.category_topics, name='category_topics'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topics/search/<str:name>/', views.topic_search, name='topic_search'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('users/posts/', views.user_posts, name='user_posts'),
    path('posts/<int:pk>/update/', views.post_update, name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
]
