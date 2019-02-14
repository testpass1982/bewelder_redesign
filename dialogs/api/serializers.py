from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from dialogs.models import Dialog, Membership, Message


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = get_user_model()
        fields = 'id', 'name'


class DialogSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    creator = serializers.UUIDField(format='hex_verbose', write_only=True)
    opponent = serializers.UUIDField(format='hex_verbose', write_only=True)
    text = serializers.CharField(write_only=True)

    class Meta:
        model = Dialog
        fields = 'id', 'creator', 'opponent', 'members', 'vacancy', 'theme', 'text'

    def validate_opponent(self, value):
        """ Check that the user with id=value exists """
        user = get_user_model().objects.filter(pk=value)
        if not user.exists():
            raise serializers.ValidationError('no user with given id')
        return value

    def validate_creator(self, value):
        return self.validate_opponent(value)

    def validate(self, data):
        if data['creator'] == data['opponent']:
            raise serializers.ValidationError('creator and opponent must be different')
        return super().validate(data)

    def create(self, validated_data):
        UserModel = get_user_model()
        creator = get_object_or_404(UserModel, pk=validated_data['creator'])
        opponent = get_object_or_404(UserModel, pk=validated_data['opponent'])
        dialog = Dialog.objects.create(
            vacancy=validated_data['vacancy'],
            theme=validated_data['theme'],
        )
        Membership.objects.create(
            user=creator,
            dialog=dialog,
            last_check=timezone.now(),
            is_creator=True,
        )
        Membership.objects.create(
            user=opponent,
            dialog=dialog,
            last_check=None,
            is_creator=False,
        )
        return dialog


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'
