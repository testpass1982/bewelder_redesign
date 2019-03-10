from rest_framework import routers

from dialogs.api import views

from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class CustomRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}_list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'post': 'create_msg',
                'delete': 'leave_dialog',
            },
            name='{basename}_detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
    ]


router = CustomRouter()
router.register(r'dialogs', views.DialogView)

app_name = 'dialogs_api'
urlpatterns = router.urls
