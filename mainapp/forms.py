from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='USER NAME', required=True,
                               widget=forms.TextInput(attrs={'placeholder': "User Name"}))

    password = forms.CharField(label='PASSWORD', required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': "Passsword"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='USER NAME', required=True,
                               widget=forms.TextInput(attrs={'placeholder': "User Name"}))

    password = forms.CharField(label='PASSWORD', required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': "Passsword"}))

    confirm_password = forms.CharField(label='CONFIRM PASSWORD', required=True,
                                       widget=forms.PasswordInput(attrs={'placeholder': "Confirm Passsword"}))


class UserProfileForm(forms.Form):
    OPTIONS = (
        ('', 'Select State'),
        ('TX', 'Texas'),
        ('NY', 'New York'),
        ('SD', 'South Dakota'),
        ('ND', 'North Dakota'),
        ('CA', 'California'),
    )
    fullname = forms.CharField(label='Full Name', required=False, max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': "Full Name"}))

    address_1 = forms.CharField(label='Address 1', required=False, max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': "Address 1"}))

    address_2 = forms.CharField(label='Address 2', required=False, max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': "Address 2"}))

    city = forms.CharField(label='City', required=False, max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': "City"}))

    state = forms.ChoiceField(
        required=False, choices=OPTIONS)

    zip = forms.CharField(label='Zip', required=False, max_length=9, min_length=5,
                          widget=forms.TextInput())


class FuelQUoteForm(forms.Form):

    gallonreq = forms.CharField(required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}))

    deladdress = forms.CharField(required=False, disabled=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    deliverydate = forms.CharField(required=False,
                                   widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}))

    suggprice = forms.CharField(required=False, disabled=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))

    deuamount = forms.CharField(required=False, disabled=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))
