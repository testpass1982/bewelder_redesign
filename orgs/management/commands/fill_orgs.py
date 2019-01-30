import csv
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from orgs.models import Employer, City, Region


CSV_PATH = 'orgs/csv/employers.csv'


def create_employer_from_dict(employer_dict):
    try:
        region_ = Region.objects.get(name=employer_dict['region'])
    except ObjectDoesNotExist:
        region_ = Region.objects.create(name=employer_dict['region'])
        print('Создан регион: {0}'.format(region_))

    try:
        city_ = City.objects.get(name=employer_dict['city'], region=region_)
    except ObjectDoesNotExist:
        city_ = City.objects.create(name=employer_dict['city'], region=region_)
        print('Создан город: {0}'.format(city_))

    try:
        employer_data = {
            'name': employer_dict['name'],
            'short_name': employer_dict['short_name'],
            'inn': employer_dict['inn'],
            'city': city_,
            'logo': employer_dict['logo'],
            'site': employer_dict['site'],
            'phone': employer_dict['phone'],
            'email': employer_dict['email'],
        }
        employer_ = Employer.objects.create(**employer_data)
        print('Создан работодатель: {0}'.format(employer_))
    except:
        print('Ошибка создания: {0}'.format(employer_dict))


def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    for line in reader:
        create_employer_from_dict(line)


class Command(BaseCommand):
    help = 'Команда создает в БД объекты классов Region, City, Employer.'

    def handle(self, *args, **options):

        print('Очистка БД')
        print(Employer.objects.all().delete())
        print(City.objects.all().delete())
        print(Region.objects.all().delete())

        print('Чтение CSV')
        with open(CSV_PATH) as csv_obj:
            csv_dict_reader(csv_obj)
