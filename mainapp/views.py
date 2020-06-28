from .forms import LoginForm, RegisterForm, UserProfileForm, FuelQUoteForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib import messages


class PriceModule:
    suggprice = 125

    def get_price(self):
        return self.suggprice


def login(request):
    initial_data = {'username': 'demouser', 'password': '12345'}

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == '12345':
            return HttpResponseRedirect('/quote')
        else:
            messages.error(request, "Invalid Password!")
    else:
        form = LoginForm(initial=initial_data)

    return render(request, 'login.html', {'form': form.as_p})


def register(request):
    initial_data = {'username': 'newuser',
                    'password': '', 'confirm_password': ''}

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            return HttpResponseRedirect('/create_profile')
        else:
            messages.error(request, "Password did not match!")
    else:
        form = RegisterForm(initial=initial_data)

    return render(request, 'register.html', {'form': form.as_p})


def user_profile(request):
    initial_data = {'fullname': 'New User', 'address_1': 'Houston, Texas',
                    'address_2': 'Houston, Texas', 'city': 'Houston', 'state': 'TX', 'zip': '123456'}

    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        if form.is_valid():
            if (is_fullname_valid(form.cleaned_data['fullname']) and
                is_address_valid(form.cleaned_data['address_1']) and
                is_address2_valid(form.cleaned_data['address_2']) and
                is_city_valid(form.cleaned_data['city']) and
                is_state_valid(form.cleaned_data['state']) and
                    is_zip_valid(form.cleaned_data['zip'])):
                return HttpResponseRedirect('/quote')
            else:
                messages.error(request, "Data you entered is not valid!")

    else:
        form = UserProfileForm(initial=initial_data)

    return render(request, 'user-profile.html', {'form': form.as_p})


def fuel_quote(request):
    data = {'gallonreq': '2000', 'deladdress': 'Houston, Texas',
            'deliverydate': '2020-06-27', 'suggprice': '145.59', 'deuamount': '290000'}
    if request.method == 'POST':
        form = FuelQUoteForm(request.POST)

        if form.is_valid() and int(form.cleaned_data['gallonreq']) > 0:
            return HttpResponseRedirect('/history')
        else:
            messages.error(request, "Data you entered is not valid!")

    else:
        form = FuelQUoteForm(initial=data)

    return render(request, 'fuel-quote.html', {'form': form, 'loginuser': 'demouser', 'quote_active': True})


def fuel_quote_history(request):
    data = [{"id": 1, "req_gallons": 152,
             "del_address": "Houston, Texas", "delivery_date": "July 1, 2020", "sugg_price": 150, "total_amount": 0},
            {"id": 2, "req_gallons": 140,
             "del_address": "San Francisco, California", "delivery_date": "July 2, 2020", "sugg_price": 160, "total_amount": 0},
            {"id": 3, "req_gallons": 600,
             "del_address": "Brooklyn, New York", "delivery_date": "July 3, 2020", "sugg_price": 170, "total_amount": 0},
            {"id": 4, "req_gallons": 582,
             "del_address": "Manhattan, New York", "delivery_date": "July 4, 2020", "sugg_price": 180, "total_amount": 0},
            {"id": 5, "req_gallons": 156,
             "del_address": "Austin, Texas", "delivery_date": "July 5, 2020", "sugg_price": 190, "total_amount": 0},
            {"id": 6, "req_gallons": 175,
             "del_address": "Dallas, Texas", "delivery_date": "July 6, 2020", "sugg_price": 180, "total_amount": 0}]
    if request.method == 'GET':
        return render(request, 'fuel-quote-history.html', {'data': data, 'loginuser': 'demouser', 'history_active': True})


def is_fullname_valid(fullname):
    return len(fullname) > 0 and len(fullname) <= 50


def is_address_valid(address):
    return len(address) > 0 and len(address) <= 100


def is_address2_valid(address):
    return len(address) <= 100


def is_city_valid(city):
    return len(city) > 0 and len(city) <= 100


def is_state_valid(state):
    return len(state) == 2


def is_zip_valid(zip):
    return len(zip) > 4 and len(zip) <= 9
