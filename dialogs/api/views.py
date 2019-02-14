from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dialogs.api.serializers import DialogSerializer, MessageSerializer
from dialogs.models import Dialog, Message

User = get_user_model()


class DialogView(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer

    def create(self, request, *args, **kwargs):
        """
        data schema
        {
            creator: uuid,
            opponent: uuid,
            vacancy: id,
            theme: str,
            text: str
        }
        """
        data = request.data
        data['creator'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        dialog = serializer.save()

        Message.objects.create(
            user=request.user,
            dialog=dialog,
            text=data['text'],
        )

        setattr(serializer, 'instance', dialog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageView(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(methods=['get'], detail=True, url_name='list')
    def list_messages(self, request, pk=None):
        """
        url: api/messaging/messages/<pk>/list_messages/
        name: 'message-list'
        pk: `pk` of the `Dialog`
        """
        dialog = get_object_or_404(Dialog, pk=pk)
        messages = Message.objects.filter(dialog=dialog)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_name='post')
    def post_message(self, request, pk=None):
        """
        url: api/messaging/messages/<pk>/post_message/
        name: 'message-post'
        pk: `pk` of the `Dialog`
        """
        dialog = get_object_or_404(Dialog, pk=pk)
        data = request.data
        try:
            message = Message.objects.create(
                user=request.user,
                dialog=dialog,
                text=data['text'],
            )
            serializer = self.get_serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
