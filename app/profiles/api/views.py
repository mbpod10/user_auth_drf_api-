from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile
from .serializers import ProfileSerializer


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
