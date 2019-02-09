from haystack import indexes
from orgs.models import Employer


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
