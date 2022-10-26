from django import forms


# Form processing for Tracking search form in navbar.
class SearchForm(forms.Form):
    tracking_code = forms.UUIDField(widget=forms.TextInput(attrs={'placeholder': 'Track a Package', 'type': 'search',
                                                                  'class': 'form-control me-2'}), label='tracking_code')


class SubscribeForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=16,
                               label="minecraft_username")
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="subscriber_email")
