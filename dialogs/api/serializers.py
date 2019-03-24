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


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user.id', read_only=True)
    name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Membership
        fields = ('id', 'name', 'is_creator')


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('dialog',)


class DialogListSerializer(serializers.ModelSerializer):
    members = MemberSerializer(source='membership_set', many=True, read_only=True)

    class Meta:
        model = Dialog
        fields = 'id', 'members', 'vacancy', 'theme'


class DialogRetrieveSerializer(serializers.ModelSerializer):
    members = MemberSerializer(source='membership_set', many=True, read_only=True)
    message_set = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Dialog
        fields = '__all__'


class DialogCreateSerializer(serializers.ModelSerializer):
    opponent = serializers.UUIDField(format='hex_verbose', write_only=True)
    text = serializers.CharField(write_only=True)

    class Meta:
        model = Dialog
        fields = 'opponent', 'vacancy', 'theme', 'text'

    def validate_opponent(self, value):
        """ Check that the user with id=value exists """
        user = get_user_model().objects.filter(pk=value)
        if not user.exists():
            raise serializers.ValidationError('no user with given id')
        return value

    def create(self, validated_data):
        UserModel = get_user_model()

        creator = validated_data['creator']
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

        if opponent != creator:
            Membership.objects.create(
                user=opponent,
                dialog=dialog,
                last_check=None,
                is_creator=False,
            )
        Message.objects.create(
            user=creator,
            dialog=dialog,
            text=validated_data['text'],
        )
        return dialog
