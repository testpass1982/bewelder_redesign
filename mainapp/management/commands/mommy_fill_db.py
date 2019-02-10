
from django.core.management.base import BaseCommand
from model_mommy import mommy
from mixer.backend.django import mixer
from model_mommy.recipe import Recipe, foreign_key, seq
from vacancies.models import Vacancy, Level
from orgs.models import Employer, City, Region
from itertools import cycle
import random

employer_names = [
    'LUKOIL', 
    'TRANSNEFT', 
    'GAZPROM',
    'STROYGAZCONSULTING',
]

employer_short_names = [
    'LUK',
    'TN',
    'GP',
    'SGC',
]

regions = ['MO',
           'LEN OBL',
           'RP TATARSTAN',
           'RP BASHKIRIYA',
]

cities = ['MOSCOW',
          'SPB',
          'KAZAN',
          'UFA',
]

salaries = [
    100000,
    150000,
    200000,
    55000,
]

region = Recipe(
    Region,
    name = cycle(regions)
)

city = Recipe(
    City,
    name = cycle(cities),
    region = foreign_key(region)
)

employer = Recipe(
    Employer,
    name = cycle(employer_names),
    short_name = cycle(employer_short_names),
    city = foreign_key(city),
    site = seq('site.ru'),
    inn = seq('123456789'),
    phone = seq('8925601140'),
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        #delete all before begin cooking
        Employer.objects.all().delete()
        City.objects.all().delete()
        Region.objects.all().delete()
        Vacancy.objects.all().delete()

        #make employers
        for i in range(0, len(employer_names)):
            employer.make()
        #make levels
        mixer.cycle(4).blend(Level)
        #make vacancies
        mixer.cycle(15).blend(
                    Vacancy,
                    employer=mixer.SELECT,
                    salary_max = random.choice(salaries))
        #setting up levels
        all_vacancies = Vacancy.objects.all()
        all_levels = Level.objects.all()
        for vacancy in all_vacancies:
            vacancy.naks_att_level.add(random.choice(all_levels))

