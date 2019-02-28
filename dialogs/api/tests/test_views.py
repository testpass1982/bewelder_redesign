from django.contrib.auth import get_user_model
from django.db.models import Q
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from dialogs.models import Dialog, Membership, Message

User = get_user_model()


class DialogViewAPITestCase(APITestCase):

    def setUp(self):
        self.dialog = mixer.blend(Dialog)
        self.creator, self.opponent = mixer.cycle(2).blend(User)
        mixer.blend(Membership, dialog=self.dialog, user=self.creator, is_creator=True)
        mixer.blend(Membership, dialog=self.dialog, user=self.opponent)
        self.url_dialog_list = reverse('dialogs_api:dialog_list')
        self.url_dialog_detail = reverse('dialogs_api:dialog_detail', kwargs={'pk': self.dialog.pk})

    def test_get_dialog_list(self):
        resp = self.client.get(self.url_dialog_list, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.opponent)
        resp = self.client.get(self.url_dialog_list, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['id'], self.dialog.pk)

    def test_post_dialog_list(self):
        creator, opponent = mixer.cycle(2).blend(User)

        data = {
            'opponent': opponent.pk,
            'vacancy': None,
            'theme': 'Предложение',
            'text': 'Xотим вас нанять',
        }

        self.client.force_login(creator)
        resp = self.client.post(self.url_dialog_list, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        created_dialog = Dialog.objects.get(members=creator)
        self.assertDictEqual(resp.data, {'id': created_dialog.pk})
        # self.assertEqual(resp.data.get('theme'), data['theme'])
        created_msg = Message.objects.first()
        self.assertEqual(created_msg.user, creator)
        self.assertEqual(created_msg.text, data['text'])

    def test_post_message(self):

        msg = {'text': 'Hello world'}

        resp = self.client.post(self.url_dialog_detail, data=msg, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.creator)
        resp = self.client.post(self.url_dialog_detail, data=msg, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_permissions_unauthorized(self):
        testcases = [
            self.url_dialog_detail,
            self.url_dialog_list,
        ]
        for case in testcases:
            with self.subTest(case=case):
                resp = self.client.get(case)
                self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
                resp = self.client.post(case, data={}, format='json')
                self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_authorized(self):
        user = mixer.blend(User)
        self.client.force_login(user)

        # Проверка, что пользователь не может получить чужие диалоги
        resp = self.client.get(self.url_dialog_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

        # Проверка, что пользователь не может получить чужие сообщения
        resp = self.client.get(self.url_dialog_detail)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # Проверка, что пользователь не может отправить сообщение в чужой диалог
        msg = {'text': 'foo bar'}
        resp = self.client.post(self.url_dialog_detail, data=msg, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_leave_dialog(self):
        user = self.creator
        self.client.force_login(user)

        # Проверяем, что учавствуем в одном диалоге
        resp = self.client.get(self.url_dialog_list)
        self.assertEqual(len(resp.data), 1)

        # Покидаем (удаляемся из) диалог
        resp = self.client.delete(self.url_dialog_detail)
        self.assertEqual(resp.status_code, 204)

        # Проверяем, что участвуем в 0 диалогах
        resp = self.client.get(self.url_dialog_list)
        self.assertEqual(len(resp.data), 0)

        # Убеждаемся, что нет доступа к покинутому диалогу
        resp = self.client.get(self.url_dialog_detail)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # Убеждаемся, что не можем отправить сообщение в покинутый диалог
        resp = self.client.post(self.url_dialog_detail, data={'text': 'text'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Убеждаемся, что не можем удалиться дважды
        resp = self.client.delete(self.url_dialog_detail)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
