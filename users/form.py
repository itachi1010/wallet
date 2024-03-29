# users/forms.py




from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Card, Transaction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'date_of_birth', 'phone_number', 'identification_type', 'id_front_image', 'id_back_image', 'selfie_with_id_image', 'social_security_number']


class AdminNotificationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'cardholder_name', 'expiry_date', 'security_code', 'billing_address']


class TransactionForm(forms.ModelForm):
    # Add the choices for the bank field
    BANK_CHOICES = [
        ('bank_of_america', 'Bank of America'),
        ('wells_fargo', 'Wells Fargo'),
        ('chase', 'Chase'),
        ('bank_of_new_york_mellon', 'Bank of New York Mellon'),
        ('citigroup', 'Citigroup'),
        ('truist_bank', 'Truist Bank'),
        ('american_express', 'American Express'),
        ('deutsche_bank', 'Deutsche Bank'),
        ('dz_bank', 'DZ Bank'),
        # Add more banks as needed
    ]

    bank = forms.ChoiceField(choices=BANK_CHOICES)

    class Meta:
        model = Transaction
        fields = ['card', 'bank', 'amount']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        if user:
            # Restrict card choices to only the cards owned by the user
            self.fields['card'].queryset = Card.objects.filter(user=user)

#just added