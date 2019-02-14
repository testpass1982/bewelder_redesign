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


class MessageViewAPITestCase(APITestCase):
    def setUp(self):
        self.user_one = mixer.blend(User)
        self.user_two = mixer.blend(User)
        self.dialog = mixer.blend(Dialog)
        Membership.objects.create(
            user=self.user_one,
            dialog=self.dialog,
            is_creator=True,
        )
        Membership.objects.create(
            user=self.user_two,
            dialog=self.dialog,
            is_creator=False,
        )
        self.message_one = Message.objects.create(
            user=self.user_one,
            dialog=self.dialog,
            text='It is a test message.'
        )
        self.message_two = Message.objects.create(
            user=self.user_two,
            dialog=self.dialog,
            text='It is an answer.'
        )
        return super().setUp()

    def test_list_messages(self):
        url = reverse('dialogs_api:message-list', kwargs={'pk': self.dialog.pk})
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)
        self.assertEqual(
            resp.data[0]['text'],
            self.message_one.text
        )
        self.assertEqual(
            resp.data[1]['text'],
            self.message_two.text
        )

        url = reverse('dialogs_api:message-list', kwargs={'pk': 9876})
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_message(self):
        msg = {
            'text': 'new message'
        }
        url = reverse(
            'dialogs_api:message-post',
            kwargs={'pk': self.dialog.pk},
        )
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        resp = self.client.post(url, data=msg, format='json')
        self.assertEqual(resp.status_code, status.HTTP_412_PRECONDITION_FAILED)

        self.client.force_login(self.user_one)
        resp = self.client.post(url, data=msg, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['text'], msg['text'])
        self.assertEqual(
            Message.objects.filter(dialog=self.dialog).count(),
            3
        )
