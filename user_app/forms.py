from django import forms


class SignUpForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=250)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class LogInForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=250)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
