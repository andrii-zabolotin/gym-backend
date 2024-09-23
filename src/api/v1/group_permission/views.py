from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, authentication, status
from rest_framework.response import Response

from api.auth.permissions import IsSuperUser
from api.v1.group_permission.serializers import CreateGroupSerializer, GroupSerializer, PermissionSerializer, \
    UserGroupSerializer, UserGroupCreateSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    Manage user groups
    """
    queryset = Group.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CreateGroupSerializer

        return GroupSerializer


class PermissionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Permission.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSuperUser]
    serializer_class = PermissionSerializer


class UserGroupViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSuperUser]
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserGroupSerializer

        return UserGroupCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(get_user_model(), id=request.data.get("user_id", None))
        group = get_object_or_404(Group, id=request.data.get("group_id", None))

        if group in user.groups.all():
            return Response({"detail": "User already has this group."}, status=status.HTTP_400_BAD_REQUEST)

        user.groups.add(group)
        return Response(UserGroupSerializer(instance=user).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id", None)
        group_id = kwargs.get("group_id", None)

        data = {
            "user_id": user_id,
            "group_id": group_id
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(get_user_model(), id=user_id)
        group = get_object_or_404(Group, id=group_id)

        if group in user.groups.all():
            user.groups.remove(group)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'User is not a member of this group'}, status=status.HTTP_400_BAD_REQUEST)
