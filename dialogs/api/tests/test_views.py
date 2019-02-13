from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from dialogs.models import Dialog, Membership, Message

User = get_user_model()


class DialogViewAPITestCase(APITestCase):
    url = reverse('dialogs_api:dialog-list')

    def test_dialogs_list_url_exists(self):
        # url = reverse('dialogs_api:dialog-list')
        resp = self.client.get(self.url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_dialog_list(self):
        for _ in range(3):
            dialog = mixer.blend(Dialog)
            mixer.cycle(2).blend(Membership, dialog=dialog)
        resp = self.client.get(self.url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 3)

    def test_post_dialog_list(self):
        creator, opponent = mixer.cycle(2).blend(User)

        data = {
            'opponent': opponent.pk,
            'vacancy': None,
            'theme': 'Предложение',
            'text': 'Xотим вас нанять',
        }

        self.client.force_login(creator)
        resp = self.client.post(self.url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data.get('theme'), data['theme'])
        created_msg = Message.objects.first()
        self.assertEqual(created_msg.user, creator)
        self.assertEqual(created_msg.text, data['text'])
