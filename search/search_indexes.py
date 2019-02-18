from haystack import indexes

from resumes.models import Resume
from vacancies.models import Vacancy
from orgs.models import Employer


class ResumeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    position = indexes.CharField(model_attr='position', null=True)
    about = indexes.CharField(model_attr='about', null=True)
    city = indexes.CharField(model_attr='city', null=True)

    def get_model(self):
        return Resume


class VacancyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    employer = indexes.CharField(model_attr='employer', null=True)
    short_description = indexes.CharField(model_attr='short_description', null=True)
    description = indexes.CharField(model_attr="description", null=True)

    def get_model(self):
        return Vacancy


class EmployerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    short_name = indexes.CharField(model_attr='short_name')
    city = indexes.CharField(model_attr='city')
    inn = indexes.CharField(model_attr='inn')
    site = indexes.CharField(model_attr='site', null=True)
    phone = indexes.CharField(model_attr='phone')
    email = indexes.CharField(model_attr='email')

    def get_model(self):
        return Employer
