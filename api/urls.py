from django.urls import path, include

from .views import ProfileView, ClinicView, ChatView, ChatList

app_name = 'api'

urlpatterns = [
    path('v1/profile', ProfileView.as_view(), name="profile"),
    path('v1/clinic', ClinicView.as_view(), name="clinic"),
    path('v1/chat', ChatView.as_view(), name="chat"),
    path('v1/chat/conversation', ChatList.as_view(), name="chat_list")
]