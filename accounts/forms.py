from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.constants import ACCOUNT_TYPE, GENDER_TYPE
from django.contrib.auth.models import User
from accounts.models import UserAddress, UserBankAccount

class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        # password1 mane normal password and password2 mane confirm_password
        fields = [
            'username', 'first_name', 'last_name', 'email', 'account_type',
            'gender', 'birth_date', 'street_address', 'city', 'postal_code',
            'country', 'password1', 'password2'
        ]

        # form.save()
    def save(self, commit=True):
        our_user = super().save(commit=False) # super keyward deye amra user, field er moddhe jei data gula dece oi gula inherit kore neye aslam abong 
            # commit = False kore bollam ei data gula akhn data base e save korbo na

        if commit == True:
            our_user.save() #user model e data save korlam
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user = our_user,
                street_address = street_address,
                city = city,
                postal_code = postal_code,
                country = country
            )
                
            UserBankAccount.objects.create(
                user = our_user,
                account_type = account_type,
                gender = gender,
                birth_date = birth_date, 
                account_no = 1000000 + our_user.id
            )
            return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            # print(field)
            self.fields[field].widget.attrs.update({

                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gary-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class UserUpdateForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # amader model form er moddhe jei field gula ase oi gula super key ward deye inherite kore neye aslam

        for field in self.fields:
            self.fields[field].widget.attrs.update({

                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gary-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        # jodi account thake
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserBankAccount.DoesNotExist:
                user_account = None
                user_address = None
            
            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initail = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initail = user_address.postal_code
                self.fields['country'].initail = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False) # super key ward deye amra user, field er moddhe jei data gula dece oi gula inherite kore neye aslam abong 
        # commit flase kore bollam akhon data gula database e save korbo na

        if commit:
            user.save()

            user_account, created = UserBankAccount.objects.get_or_create(user=user) # jodi account thake taile user_account e jabe
            # r jodi na thake tobe created er moddhe jabe
            user_address , created = UserAddress.objects.get_or_create(user=user)# jodi account thake taile user_account e jabe
            # r jodi na thake tobe created er moddhe jabe

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
