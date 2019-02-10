from haystack import indexes

from resumes.models import Resume


class ResumeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    position = indexes.CharField(model_attr='position', null=True)
    about = indexes.CharField(model_attr='about', null=True)
    city = indexes.CharField(model_attr='city', null=True)

    def get_model(self):
        return Resume
