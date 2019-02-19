"""The URL configuration of LearnLogs"""

from django.urls import path
from . import views
# from django.conf.urls import url

urlpatterns = [
    # HomePage
    path('', views.index, name='index'),

    # The page shows the topics
    path('topics/', views.topics, name='topics'),

    # The page shows the entries of a topic
    path('topics/<topic_id>/', views.topic, name='topic'),
    # url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # The page is used to add new topic
    path('new_topic/', views.new_topic, name='new_topic'),

    # The page is used to add new entry
    path('new_entry/<topic_id>/', views.new_entry, name='new_entry'),

    # The page is used to edit an entry
    path('edit_entry/<entry_id>/', views.edit_entry, name='edit_entry'),
]
