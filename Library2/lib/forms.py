from django import forms
from django.contrib.auth.models import User
from .models import Knjiga, Lokacija

#prijava
class LoginForm(forms.Form):
  username = forms.CharField(label='Uporabniško ime:', max_length=100, widget=forms.TextInput(attrs={'class' : 'textfield'}))
  password = forms.CharField(label='Geslo', max_length=100, widget=forms.PasswordInput(attrs={'class' : 'textfield'}))

#registracija
class RegistrationForm(forms.Form):
  first_name = forms.CharField(label='Ime:', max_length=100, widget=forms.TextInput(attrs={'class' : 'textfield'}))
  last_name = forms.CharField(label='Priimek:', max_length=100, widget=forms.TextInput(attrs={'class' : 'textfield'}))
  username = forms.RegexField(regex=r'^\w+$', required=True, max_length=30, widget=forms.TextInput(attrs={'class' : 'textfield'}),
                        label="Uporabniško ime:", error_messages={'uporabniško ime': 'Uporabite lahko črke, številke ali podčrtaje.'})
  email = forms.EmailField(label="Email naslov:", required=True, max_length=30, widget=forms.TextInput(attrs={'class' : 'textfield'}))
  password1 = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput(attrs={'class' : 'textfield'}),
                              label="Geslo:")
  password2 = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput(attrs={'class' : 'textfield'}),
                              label="Ponovi geslo:")

  def clean_username(self):
    try:
      user = User.objects.get(username__iexact=self.cleaned_data['username'])
    except User.DoesNotExist:
      return self.cleaned_data['username']
    print("username")
    raise forms.ValidationError("To uporabniško ime že obstaja.")

  def clean(self):
    if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
      if self.cleaned_data['password1'] != self.cleaned_data['password2']:
        raise forms.ValidationError("Gesli se ne ujemata.")
    return self.cleaned_data


#dodaj
class DodajForm(forms.ModelForm):
    class Meta:
        model = Knjiga
        fields = ['avtorji', 'naslov', 'lokacija']


#profil
class MenjajUsername(forms.Form):
    new_username = forms.CharField(label='Novo uporabniško ime:', max_length=100,
                                   widget=forms.TextInput(attrs={'class' : 'textfield'}))

    def clean_username(self):
        username = self.cleaned_data['new_username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("To uporabniško ime že obstaja.")
        return username

#profil
class MenjajGeslo(forms.Form):
    password1 = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput(attrs={'class' : 'textfield'}),
                              label="Novo geslo:")
    password2 = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput(attrs={'class' : 'textfield'}),
                              label="Ponovi geslo:")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Gesli se ne ujemata.")
        return self.cleaned_data

#administrator
class AdminForm(forms.ModelForm):
    class Meta:
        model = Lokacija
        fields = ['nadstropje', 'omara', 'polica']