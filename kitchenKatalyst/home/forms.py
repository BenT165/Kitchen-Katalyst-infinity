from django import forms
from django.forms import ModelForm
from .models import User
from .models import Grocery
from .models import Recipe
from django.utils import timezone
from django.core.exceptions import ValidationError
import re



UNIT_CHOICES = (
        ('', 'Select Unit'),  # Default empty option
        ('none', 'None'),
        ('cup', 'Cup'),
        ('tablespoon', 'Tablespoon'),
        ('teaspoon', 'Teaspoon'),
        ('pound', 'Pound'),
        ('ounce', 'Ounce'),
        ('kilogram', 'Kilogram'),
        ('gram', 'Gram'),
        ('gallon', 'Gallon'),
        ('quart', 'Quart'),
        ('pint', 'Pint'),
        ('liter', 'Liter'),
        ('milliliter', 'Milliliter'),
)


#form to Register User
class UserForm(ModelForm):

    class Meta:
        model = User

        #get fields for model
        fields = ('first_name','last_name','email', 'username', 'password', 'date_reminder')
        exclude = ['last_login']
    
        def clean_first_name(self):
            first_name = self.cleaned_data.get('first_name')
            # Perform custom validation for username, if needed
            # Example: Ensure username is unique
            
            return first_name

        def clean_last_name(self):
            last_name = self.cleaned_data.get('last_name')
            # Perform custom validation for username, if needed
            # Example: Ensure username is unique
            
            return last_name

        def clean_email(self):
            email = self.cleaned_data.get('email')
            # Perform custom validation for username, if needed
            # Example: Ensure username is unique
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already in use.')

            if re.search(r'[\';"]', email):
                raise forms.ValidationError('Username contains illegal characters.')
            
            return email

        def clean_username(self):
            username = self.cleaned_data.get('username')
            # Perform custom validation for username, if needed
            # Example: Ensure username is unique
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('This username is already in use.')

            if re.search(r'[\';"]', username):
                raise forms.ValidationError('Username contains illegal characters.')

            return username

      

        


#form to add grocery item
class GroceryForm(ModelForm):

    unit = forms.ChoiceField(choices=UNIT_CHOICES, required=False)

    class Meta:
        model = Grocery

        #get fields for Grocery from main.html webpage
        fields = ('quantity', 'unit', 'name',  'expiration_date')

        widgets = {
            'quantity': forms.TextInput(attrs={'type':'number', 'class': 'form-control', 'placeholder':'Quantity.', 'min':'1', 'pattern':'[0-9]+', 'id':'eQuantity', 'style': 'height: 40px'}),
            'unit': forms.Select(choices=UNIT_CHOICES, attrs={'class': 'form-control','placeholder': 'type', 'id':'eUnit', 'class':'eUnit', 'style': 'height: 40px'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grocery Item name', 'id':'eName','style': 'height: 40px'}),
            'expiration_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'MM/DD/YYYY', 'id':'eExpDate', 'style': 'height: 40px'}),
        }

#form to Register Recipe
class RecipeForm(ModelForm):

    class Meta:
        model = Recipe

        #get fields for model
        fields = ('name', 'instructions')
    


