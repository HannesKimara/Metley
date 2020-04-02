from django.urls import path, include

from .views import ProfileView, ClinicView

app_name = 'api'

urlpatterns = [
    path('v1/profile', ProfileView.as_view(), name="profile"),
    path('v1/clinic', ClinicView.as_view(), name="clinic")
]