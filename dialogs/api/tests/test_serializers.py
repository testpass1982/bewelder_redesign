from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework import serializers
from rest_framework.test import APITestCase

from dialogs.api.serializers import (
    DialogListSerializer,
    DialogCreateSerializer,
    DialogRetrieveSerializer,
    UserSerializer,
)
from dialogs.models import Dialog

User = get_user_model()


class DialogCreateSerializerAPITestCase(APITestCase):
    def setUp(self):
        self.creator = mixer.blend(User)
        self.opponent = mixer.blend(User)
        return super().setUp()

    def test_validate_opponent(self):
        serializer = DialogCreateSerializer(data={})
        temp_user = mixer.blend(User)
        temp_user_id = temp_user.pk
        temp_user.delete()

        with self.assertRaises(serializers.ValidationError):
            serializer.validate_opponent(temp_user_id)

        self.assertEqual(
            serializer.validate_opponent(self.opponent.pk),
            self.opponent.pk
        )

    def test_create(self):
        data = {
            'opponent': self.opponent.pk,
            'vacancy': None,
            'theme': 'Есть тема',
            'text': 'Приходите к нам на работу',
        }
        serializer = DialogCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save(creator=self.creator)

        self.assertEqual(Dialog.objects.count(), 1)
        dialog = Dialog.objects.first()
        self.assertEqual(dialog.theme, data['theme'])
        self.assertEqual(dialog.members.count(), 2)
        self.assertEqual(dialog.message_set.count(), 1)
