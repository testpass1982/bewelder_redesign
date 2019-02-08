from django import forms

import haystack.forms as hay_forms
from haystack.utils.app_loading import haystack_get_model


class SearchForm(hay_forms.SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["models"] = forms.ChoiceField(
            choices=hay_forms.model_choices(),
            required=False,
            label='Искать',
            widget=forms.RadioSelect,
        )

    def get_model(self):
        if self.is_valid():
            model = self.cleaned_data['models']
            if model:
                return haystack_get_model(*model.split("."))

    def search(self):
        sqs = super().search()
        search_model = self.get_model()
        if search_model:
            return sqs.models(search_model)
        return sqs
