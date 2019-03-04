from rest_framework import routers
from vacancies.viewsets import VacancyViewSet
router = routers.DefaultRouter()

router.register(r'', VacancyViewSet)