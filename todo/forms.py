from django import forms
from django.contrib.auth.models import User
from django.db.models import Q


class AddUserForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email')

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist")
        return user
