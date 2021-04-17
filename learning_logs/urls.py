"""Defines urls patterns for learning_log"""

from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [
    # homepage
    path("", views.index, name='index'),

    # page that displays all available topics
    path("topics/", views.topics, name="topics"),

    # page showing individual topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # page to create a new topic
    path('new_topic/', views.new_topic, name='new_topic'),

    # page to add a new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
]
