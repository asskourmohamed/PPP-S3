from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

from django.contrib.auth.forms import AuthenticationForm
class InscriptionForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )
    type_utilisateur = forms.ChoiceField(
        choices=Utilisateur.TYPE_UTILISATEUR,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    niveau_langue_signes = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': '1', 'max': '5'})
    )
    
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'type_utilisateur', 'niveau_langue_signes', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'email', 'bio', 'avatar_personnalise', 'niveau_langue_signes')
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'niveau_langue_signes': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': '1', 'max': '5'}),
        }



class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Votre nom d\'utilisateur',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Votre mot de passe'
        })
    )