from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from profiles.api.permissions import IsOwnerOrReadOnly, IsOwnProfileOrReadOnly
from profiles.api.serializers import (AvatarSerializer,
                                      ProfileSerializer,
                                      ProfileStatusSerializer)
from profiles.models import Profile, ProfileStatus


class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile_object = self.request.user.profile
        return profile_object


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]

    """
    filter_backends = [SearchFilter]
    search_fields = ['city']
    """

    def get_queryset(self):
        queryset = Profile.objects.all()
        city = self.request.query_params.get("city", None)
        id = self.request.query_params.get("id", None)
        # print(self.request.query_params)
        if city is not None:
            queryset = queryset.filter(city=city)
            if id is not None:
                """ http://127.0.0.1:8000/api/profiles/?city=Hamilton&id=1 """
                queryset = queryset.filter(id=id)
        return queryset


class ProfileStatusViewSet(ModelViewSet):
    serializer_class = ProfileStatusSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """ http://127.0.0.1:8000/api/status/?username=brock """
        queryset = ProfileStatus.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            """ https://www.django-rest-framework.org/api-guide/filtering/ """
            """ same as ProfileStatus.user_profile.user.username """
            queryset = queryset.filter(user_profile__user__username=username)
        return queryset

    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile=user_profile)
