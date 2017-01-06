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
    #avtorji = forms.CharField(label='Avtorji:', max_length=100, widget=forms.TextInput(attrs={'class': 'textfield'}))
    #naslov = forms.CharField(label='Naslov:', max_length=100, widget=forms.TextInput(attrs={'class': 'textfield'}))
    #lokacija = forms.ChoiceField(label='Lokacija:', choices=[ l for l in Lokacija.objects.all() ], widget=forms.Select(attrs={'class' : 'textfield'}))