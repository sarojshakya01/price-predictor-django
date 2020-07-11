from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .models import *
from .forms import LoginForm, RegisterForm, UserProfileForm, FuelQUoteForm


class PriceModule:
    suggprice = 125

    def get_price(self):
        return self.suggprice


def login(request):
    initial_data = {'username': '', 'password': ''}

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid() and is_username_valid(form.cleaned_data['username']) and is_password_valid(form.cleaned_data['password']):
            userexist = UserCredentials.objects.filter(
                username=form.cleaned_data['username'], password=form.cleaned_data['password']).exists()

            if userexist:
                user = UserCredentials.objects.get(
                    username=form.cleaned_data['username'])

                if Sessions.objects.filter(
                        userid=user.userid).exists():
                    session = Sessions.objects.get(userid=user.userid)
                    session.status = True
                    session.save()

                else:
                    session = Sessions(userid=user.userid, status=True)
                    session.save()

                request.session['id'] = str(user.userid)
                return HttpResponseRedirect('/quote')
            else:
                messages.error(request, "Invalid Username or Password!")
        else:
            messages.error(request, "Invalid Username or Password!")
    else:
        form = LoginForm(initial=initial_data)

    return render(request, 'login.html', {'form': form.as_p})


def logout(request):

    if request.method == 'GET':
        user = UserCredentials.objects.get(
            userid=int(request.session['id']))

        if Sessions.objects.filter(
                userid=user.userid).exists():
            session = Sessions.objects.get(userid=user.userid)
            session.status = False
            session.save()
        return HttpResponseRedirect('/login')


def register(request):
    initial_data = {'username': '',
                    'password': '', 'confirm_password': ''}
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid() and len(form.cleaned_data['password']) > 5 and form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            request.session['username'] = form.cleaned_data['username']
            request.session['password'] = form.cleaned_data['password']

            return HttpResponseRedirect('/create_profile')
        else:
            messages.error(
                request, "Short Password or Password did not match!")
    else:
        form = RegisterForm(initial=initial_data)

    return render(request, 'register.html', {'form': form.as_p})


def user_profile(request):
    initial_data = {'fullname': '', 'address_1': '',
                    'address_2': '', 'city': '', 'state': '', 'zip': ''}

    if request.method == 'POST':

        form = UserProfileForm(request.POST)
        valid = form.is_valid()
        valid &= is_fullname_valid(form.cleaned_data['fullname'])
        valid &= is_address_valid(form.cleaned_data['address_1'])
        valid &= is_address2_valid(form.cleaned_data['address_2'])
        valid &= is_city_valid(form.cleaned_data['city'])
        valid &= is_state_valid(form.cleaned_data['state'])
        valid &= is_zip_valid(form.cleaned_data['zip'])
        valid &= len(request.session['username']) > 0
        valid &= len(request.session['password']) > 0
        if (valid):

            user = UserCredentials(
                username=request.session['username'],
                password=request.session['password'],
                confirm_password=request.session['password'])
            user.save()
            request.session.flush()

            if (ClientInformations.objects.filter(userid=user).exists()):
                userinfo = ClientInformations.objects.get(userid=user)
                userinfo.fullname = form.cleaned_data['fullname']
                userinfo.address1 = form.cleaned_data['address_1']
                userinfo.address2 = form.cleaned_data['address_2']
                userinfo.city = form.cleaned_data['city']
                userinfo.state = form.cleaned_data['state']
                userinfo.zipcode = form.cleaned_data['zip']
                userinfo.save()
            else:
                userinfo = ClientInformations(
                    userid=user,
                    fullname=form.cleaned_data['fullname'],
                    address1=form.cleaned_data['address_1'],
                    address2=form.cleaned_data['address_2'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    zipcode=form.cleaned_data['zip'])
                userinfo.save()

            return HttpResponseRedirect('/login')
        else:
            messages.error(request, "Data you entered is not valid!")

    else:
        form = UserProfileForm(initial=initial_data)

    return render(request, 'user-profile.html', {'form': form.as_p})


def fuel_quote(request):
    session = False
    user = int(request.session['id'])
    session_exist = Sessions.objects.filter(
        userid=user).exists()
    if session_exist:
        session = Sessions.objects.get(
            userid=user).status
    if session:
        userinfo = ClientInformations.objects.get(userid=user)

        data = {'gallonreq': '', 'deladdress': userinfo.address1,
                'deliverydate': str(datetime.today().strftime('%Y-%m-%d')), 'suggprice': '', 'deuamount': ''}

        if request.method == 'POST':
            form = FuelQUoteForm(request.POST)

            if form.is_valid() and int(form.cleaned_data['gallonreq']) > 0:
                form.cleaned_data['suggprice'] = '0'
                form.cleaned_data['deuamount'] = '0'
                fuelquote = FuelQuotes(
                    userid=UserCredentials.objects.get(
                        userid=user),  # hardcode for now

                    req_gallons=int(form.cleaned_data['gallonreq']),
                    del_address=form.cleaned_data['deladdress'],
                    delivery_date=datetime.strptime(
                        form.cleaned_data['deliverydate'], '%Y-%m-%d'),
                    sugg_price=float(form.cleaned_data['suggprice']),
                    due_amount=float(form.cleaned_data['deuamount']))
                fuelquote.save()
                return HttpResponseRedirect('/history')
            else:
                messages.error(request, "Data you entered is not valid!")

        else:
            form = FuelQUoteForm(initial=data)

        return render(request, 'fuel-quote.html', {'form': form, 'loginuser': 'demouser', 'quote_active': True})
    else:
        return HttpResponseRedirect('/login')


def fuel_quote_history(request):
    session = False
    user = int(request.session['id'])
    session_exist = Sessions.objects.filter(
        userid=user).exists()
    if session_exist:
        session = Sessions.objects.get(
            userid=user).status
    if session:
        rows = FuelQuotes.objects.filter(userid=user).order_by("quoteid")
        data = []
        for row in rows:
            a = {'id': row.quoteid, "req_gallons": row.req_gallons,
                 "del_address":  row.del_address, "delivery_date":  row.delivery_date, "sugg_price":  row.sugg_price, "total_amount": 0}
            data.append(a)

        if request.method == 'GET':
            return render(request, 'fuel-quote-history.html', {'data': data, 'loginuser': 'demouser', 'history_active': True})
    else:
        return HttpResponseRedirect('/login')


def is_username_valid(username):
    return len(username) > 0 and len(username) <= 50


def is_password_valid(password):
    return len(password) > 5 and len(password) <= 50


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
