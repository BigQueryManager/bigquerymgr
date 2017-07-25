from django import forms
from queries.models import Queries


class QueryForm(forms.ModelsForm):
    def __init__():
    query_name = forms.CharField(label='Query name', max_length=100)