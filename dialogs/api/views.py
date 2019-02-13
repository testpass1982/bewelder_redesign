from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from dialogs.api.serializers import DialogSerializer
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
