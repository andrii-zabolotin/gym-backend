from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.permissions import IsAdministratorOrSuperUser
from api.v1.user.serializers import UserSerializer, LimitedUserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    permission_classes = []

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserStaffListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='group',
                description='Filter users by group (e.g., "Тренери" or "Масажисти")',
                required=True,
                type=str
            )
        ],
        responses={
            200: LimitedUserSerializer(many=True),
            400: OpenApiParameter(name="error", description="Group parameter is required", required=False, type=str),
            404: OpenApiParameter(name="error", description="Group not found or No users found in this group",
                                  required=False, type=str),
        }
    )

    def get(self, request):
        group = request.query_params.get('group')

        if not group:
            return Response({"error": "Group parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        if group not in ["Тренери", "Масажисти"]:
            return Response({"error": "Group parameter is should be 'Тренери' or 'Масажисти'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group_obj = Group.objects.get(name=group)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        users = get_user_model().objects.filter(groups=group_obj)

        if not users.exists():
            return Response({"error": "No users found in this group"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LimitedUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdministratorOrSuperUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='phone', description='User phone number', required=False, type=str),
            OpenApiParameter(name='email', description='User email address', required=False, type=str),
            OpenApiParameter(name='user_id', description='User ID', required=False, type=int),
        ],
        responses={
            200: UserSerializer,
            404: OpenApiParameter(name="error", description="User not found", required=False, type=str),
        },
    )
    def get(self, request):
        phone = request.query_params.get('phone')
        email = request.query_params.get('email')
        user_id = request.query_params.get('user_id')

        user = None
        if user_id:
            user = get_user_model().objects.filter(id=user_id).first()
        if phone:
            user = get_user_model().objects.filter(phone=phone).first()
        if email:
            user = get_user_model().objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]
