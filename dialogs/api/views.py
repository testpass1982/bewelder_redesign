from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from dialogs.api.permissions import IsInDialog
from dialogs.api.serializers import (DialogCreateSerializer,
                                     DialogListSerializer,
                                     DialogRetrieveSerializer,
                                     MessageSerializer)
from dialogs.models import Dialog, Message

User = get_user_model()


class DialogView(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Dialog.objects.none()
    serializer_class = DialogListSerializer
    permission_classes = (IsInDialog,)

    action_serializers = {
        'create': DialogCreateSerializer,
        'list': DialogListSerializer,
        'retrieve': DialogRetrieveSerializer,
        'create_msg': MessageSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        return Dialog.objects.filter(members=user, membership__is_active=True)

    def get_serializer_class(self):
        return self.action_serializers.get(
            self.action,
            DialogListSerializer
        )

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
        output schema
        {
            id: int  # возвращает id созданного диалога
        }
        """

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        dialog = serializer.save(creator=request.user)

        return Response({'id': dialog.id}, status=status.HTTP_201_CREATED)

    def create_msg(self, request, pk=None):
        """
        data schema
        {
            text: str,
        }
        """
        dialog = get_object_or_404(Dialog, pk=pk)
        self.check_object_permissions(request, dialog)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, dialog=dialog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def leave_dialog(self, request, pk=None):
        dialog = get_object_or_404(Dialog, pk=pk)
        self.check_object_permissions(request, dialog)
        user = request.user
        membership = dialog.membership_set.get(user=user)
        membership.is_active = False
        membership.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
