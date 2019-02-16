from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from dialogs.api.serializers import (
    DialogCreateSerializer,
    DialogListSerializer,
    DialogRetrieveSerializer,
    MessageSerializer,
)
from dialogs.models import Dialog, Message

User = get_user_model()


class DialogView(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogListSerializer
    permission_classes = (IsAuthenticated,)

    action_serializers = {
        'create': DialogCreateSerializer,
        'list': DialogListSerializer,
        'retrieve': DialogRetrieveSerializer,
        'create_msg': MessageSerializer,
    }

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
        """

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # TODO: check creator != opponent

        dialog = serializer.save(creator=request.user)

        dialog_details = self.action_serializers['retrieve'](dialog)

        return Response(dialog_details.data, status=status.HTTP_201_CREATED)

    def create_msg(self, request, pk=None):
        """
        data schema
        {
            text: str,
        }
        """
        dialog = get_object_or_404(Dialog, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, dialog=dialog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
