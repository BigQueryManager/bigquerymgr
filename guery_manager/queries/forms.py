"""."""


from django import forms
from queries.models import Queries


class QueryForm(forms.ModelsForm):
    """Form to create a new query."""

    def __init__():
        query_name = forms.CharField(label='query', max_length=100)
