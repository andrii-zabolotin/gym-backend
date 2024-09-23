from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename',)


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions',)


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'phone', 'groups')


class UserGroupCreateSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())
    group_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Group.objects.all())


class CreateGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions', 'permission_ids',)

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids')
        group = Group.objects.create(**validated_data)
        group.permissions.set(permission_ids)
        return group

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids')
        if permission_ids:
            instance.permissions.set(permission_ids)
        return super().update(instance, validated_data)
