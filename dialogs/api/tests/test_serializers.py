from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework import serializers
from rest_framework.test import APITestCase

from dialogs.api.serializers import DialogSerializer, UserSerializer
from dialogs.models import Dialog

User = get_user_model()


class DialogSerializerAPITestCase(APITestCase):
    def setUp(self):
        self.creator = mixer.blend(User)
        self.opponent = mixer.blend(User)
        return super().setUp()

    def test_validate_opponent(self):
        serializer = DialogSerializer(data={})
        temp_user = mixer.blend(User)
        temp_user_id = temp_user.pk
        temp_user.delete()

        with self.assertRaises(serializers.ValidationError):
            serializer.validate_opponent(temp_user_id)

        self.assertEqual(
            serializer.validate_opponent(self.opponent.pk),
            self.opponent.pk
        )

    def test_validate_creator(self):
        serializer = DialogSerializer(data={})
        temp_user = mixer.blend(User)
        temp_user_id = temp_user.pk
        temp_user.delete()

        with self.assertRaises(serializers.ValidationError):
            serializer.validate_creator(temp_user_id)

        self.assertEqual(
            serializer.validate_creator(self.creator.pk),
            self.creator.pk
        )

    def test_validate(self):
        data = {
            'creator': self.creator.pk,
            'opponent': self.creator.pk,
        }
        with self.assertRaises(serializers.ValidationError):
            DialogSerializer().validate(data)

        data = {
            'creator': self.creator.pk,
            'opponent': self.opponent.pk,
        }
        self.assertDictEqual(
            DialogSerializer().validate(data),
            data
        )

    def test_create(self):
        data = {
            'creator': self.creator.pk,
            'opponent': self.opponent.pk,
            'vacancy': None,
            'theme': 'Есть тема',
            'text': 'Приходите к нам на работу',
        }
        serializer = DialogSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        
        self.assertEqual(Dialog.objects.count(), 1)
        dialog = Dialog.objects.first()
        self.assertEqual(dialog.theme, data['theme'])
        self.assertEqual(dialog.members.count(), 2)
