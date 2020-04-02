from django.urls import path, include

from .views import ProfileView

app_name = 'api'

urlpatterns = [
    path('v1/profile', ProfileView.as_view(), name="profile"),
]