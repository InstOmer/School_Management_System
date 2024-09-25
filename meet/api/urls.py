from django.urls import path
from meet.api.views import MeetListCreateView, MeetDetailView


urlpatterns = [
    path("", MeetListCreateView.as_view(), name="meet-list-create"),
    path("<int:pk>/", MeetDetailView.as_view(), name="meet-detail"),
]