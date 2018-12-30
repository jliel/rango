from django import forms
from rango.models import Page, Category


class Categoryform(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name', 'views', 'likes')

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = super().clean()
        url = self.cleaned_data.get('url')
        if not url.startswith('http://'):
            url += 'http://'
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        model = Page
        fields = ('title', 'url', 'views')
