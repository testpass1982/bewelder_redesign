from rest_framework import routers

from dialogs.api import views

router = routers.SimpleRouter()
router.register(r'dialogs', views.DialogView)

app_name = 'dialogs_api'
urlpatterns = router.urls
