from django import forms

class SiteForm(forms.Form):
    url = forms.URLField(label='URL страницы',max_length=255)
    query = forms.CharField(label='Запрос XPath',max_length=255)
