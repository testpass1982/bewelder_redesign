from django import forms

import haystack.forms as hay_forms
from haystack.utils.app_loading import haystack_get_model

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import RegexpTokenizer


try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class SearchForm(hay_forms.SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = hay_forms.model_choices()
        self.fields["models"] = forms.ChoiceField(
            choices=choices,
            required=False,
            label='Искать',
            widget=forms.RadioSelect,
            initial=choices[0][0]
        )
        self.stopwords = set(stopwords.words('russian'))
        self.stemmer = RussianStemmer()
        self.tokenizer = RegexpTokenizer(r'\w+')

    def get_model(self):
        if self.is_valid():
            model = self.cleaned_data['models']
            if model:
                return haystack_get_model(*model.split("."))
        return None

    def prepare_query(self, query_string):
        words = self.tokenizer.tokenize(query_string.lower())
        words = [
            self.stemmer.stem(word)
            for word in words
            if word not in self.stopwords
        ]
        return ' '.join(words)

    def search(self):
        if not (self.is_valid() and self.cleaned_data.get('q')):
            return self.no_query_found()

        query = self.prepare_query(self.cleaned_data['q'])

        sqs = self.searchqueryset.filter(content__contains=query)
        if self.load_all:
            sqs = sqs.load_all()

        search_model = self.get_model()
        if search_model:
            return sqs.models(search_model)
        return sqs
