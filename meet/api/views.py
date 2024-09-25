from rest_framework import generics
from meet.models import Meet
from meet.api.serializers import MeetSerializer
from meet.api.permissions import IsAdminOrTeacherOrReadOnly


class MeetListCreateView(generics.ListCreateAPIView):
    queryset = Meet.objects.all()
    serializer_class = MeetSerializer
    permission_classes = [IsAdminOrTeacherOrReadOnly]
    
    
class MeetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meet.objects.all()
    serializer_class = MeetSerializer
    permission_classes = [IsAdminOrTeacherOrReadOnly]