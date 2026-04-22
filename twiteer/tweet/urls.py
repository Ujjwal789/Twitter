from django.urls import path
from .import views
# app/urls.py
urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),        # ✅ keep this
    # path('', views.post_tweet, name='post_tweet'),      # ❌ remove duplicate
    path('create/', views.create_tweet, name='create_tweet'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
]
