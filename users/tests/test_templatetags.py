from django import forms
from django.template import Template, Context
from django.test import SimpleTestCase


class TestForm(forms.Form):
    """ Test form. """
    field_simple = forms.CharField()


class CssExtrasTestCase(SimpleTestCase):
    def test_css_class(self):
        template = Template(
            '''
            {% load css_extras %}
            {{ form.field_simple|css_class:"foo" }}
            ''')
        context = Context({'form': TestForm()})
        result = template.render(context)
        self.assertIn('class="foo"', result)

    def test_css_class_multiple(self):
        template = Template(
            '''
            {% load css_extras %}
            {{ form.field_simple|css_class:"foo bar" }}
            ''')
        context = Context({'form': TestForm()})
        result = template.render(context)
        self.assertIn('class="foo bar"', result)
