from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.permissions import IsAdministratorOrSuperUser
from api.v1.user.filters import StaffFilter
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


class UserStaffListAPIView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = LimitedUserSerializer
    authentication_classes = []
    permission_classes = []
    filterset_class = StaffFilter


class UserGetAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdministratorOrSuperUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='phone', description='User phone number', required=False, type=str),
            OpenApiParameter(name='email', description='User email address', required=False, type=str),
            OpenApiParameter(name='id', description='User ID', required=False, type=int),
        ],
        responses={
            200: UserSerializer,
            404: OpenApiParameter(name="error", description="User not found", required=False, type=str),
        },
    )
    def get(self, request):
        phone = request.query_params.get('phone')
        email = request.query_params.get('email')
        user_id = request.query_params.get('id')

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
