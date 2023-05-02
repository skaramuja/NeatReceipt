from django import forms

from accounts.models import Account


class LoginForm(forms.Form):
    """
    Form for logging in.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering.
    """
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['username', 'email']

    def clean_password2(self):
        """
        Method for validating a password.
        :return: A boolean indicating if the passwords match.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
