from datetime import datetime
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from .models import *
from .forms import LoginForm, RegisterForm, UserProfileForm, FuelQuoteForm
from .modules import Pricing


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

                request.session.flush()
                request.session['id'] = str(user.userid)
                return HttpResponseRedirect('/history')
            else:
                messages.error(request, "Invalid Username or Password!")
        else:
            messages.error(request, "Invalid Username or Password!")
    else:
        form = LoginForm(initial=initial_data)

    return render(request, 'login.html', {'form': form.as_p})


def logout(request):

    if request.method == 'GET':
        if (request.session.has_key('id')):
            user = UserCredentials.objects.get(
                userid=int(request.session['id']))

            if Sessions.objects.filter(
                    userid=user.userid).exists():
                session = Sessions.objects.get(userid=user.userid)
                session.status = False
                session.save()
            return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/login')


def register(request):
    initial_data = {'username': '',
                    'password': '', 'confirm_password': ''}
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid() and len(form.cleaned_data['password']) > 5 and form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            request.session['username'] = form.cleaned_data['username']
            request.session['password'] = form.cleaned_data['password']

            if (UserCredentials.objects.filter(username=request.session['username']).exists()):
                messages.error(
                    request, "Username already exists!")
            else:
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

        if (valid):

            if (ClientInformations.objects.filter(userid=int(request.session['id'])).exists()):
                user = int(request.session['id'])
                userinfo = ClientInformations.objects.get(userid=user)
                userinfo.fullname = form.cleaned_data['fullname']
                userinfo.address1 = form.cleaned_data['address_1']
                userinfo.address2 = form.cleaned_data['address_2']
                userinfo.city = form.cleaned_data['city']
                userinfo.state = form.cleaned_data['state']
                userinfo.zipcode = form.cleaned_data['zip']
                userinfo.save()
                return HttpResponseRedirect('/history')
            elif len(request.session['username']) > 0 and len(request.session['password']) > 0:
                username = request.session['username']

                if (UserCredentials.objects.filter(username=username).exists()):
                    user = UserCredentials.objects.get(username=username)
                    user.password = request.session['password']
                    user.confirm_password = request.session['password']
                    user.save()
                else:
                    user = UserCredentials(
                        username=request.session['username'],
                        password=request.session['password'],
                        confirm_password=request.session['password'])
                    user.save()
                request.session.flush()

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
        if request.session.has_key('username') and request.session.has_key('password'):
            form = UserProfileForm(initial=initial_data)
        elif request.session.has_key('id'):
            user = int(request.session['id'])
            session_exist = Sessions.objects.filter(
                userid=user, status=True).exists()
            if session_exist:
                userinfo = ClientInformations.objects.get(userid=user)
                initial_data['fullname'] = userinfo.fullname
                initial_data['address_1'] = userinfo.address1
                initial_data['city'] = userinfo.city
                initial_data['state'] = userinfo.state
                initial_data['zip'] = userinfo.zipcode
                form = UserProfileForm(initial=initial_data)
        else:
            return HttpResponseRedirect('/register')
    return render(request, 'user-profile.html', {'form': form.as_p})


def fuel_quote(request):
    if (request.session.has_key('id')):
        session = False
        user = int(request.session['id'])
        session_exist = Sessions.objects.filter(
            userid=user).exists()
        if session_exist:
            session = Sessions.objects.get(
                userid=user).status
            if session:
                userinfo = ClientInformations.objects.get(userid=user)
                username = UserCredentials.objects.get(userid=user).username
                state_name = States.objects.get(code=userinfo.state).name
                del_address = (userinfo.address1 + (', ' + userinfo.address2 if len(userinfo.address2) > 0 else '') + ', ' +
                               userinfo.city + ', ' + userinfo.zipcode + ', ' + state_name)
                # today = str(datetime.today().strftime('%Y-%m-%d'))
                data = {'gallonreq': '', 'deladdress': del_address,
                        'deliverydate': None, 'suggprice': '', 'deuamount': ''}

                if request.method == 'POST':
                    form = FuelQuoteForm(request.POST)

                    if form.is_valid() and int(form.cleaned_data['gallonreq']) > 0:
                        pricing = Pricing()
                        req_gallons = int(form.cleaned_data['gallonreq'])
                        sugg_price = pricing.get_suggested_price(
                            user, req_gallons)
                        sugg_price = round(sugg_price, 4)
                        amount_due = round((sugg_price * req_gallons), 4)
                        fuelquote = FuelQuotes(
                            userid=UserCredentials.objects.get(
                                userid=user),
                            req_gallons=req_gallons,
                            del_address=del_address,
                            delivery_date=datetime.strptime(
                                form.cleaned_data['deliverydate'], '%Y-%m-%d'),
                            sugg_price=sugg_price,
                            due_amount=amount_due)
                        fuelquote.save()
                        return HttpResponseRedirect('/history')
                    else:
                        messages.error(
                            request, "Data you entered is not valid!")

                else:
                    form = FuelQuoteForm(initial=data)

                return render(request, 'fuel-quote.html', {'form': form, 'loginuser': username, 'quote_active': True})
            else:
                return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/login')


def fuel_quote_history(request):
    if (request.session.has_key('id')):
        session = False
        user = int(request.session['id'])
        session_exist = Sessions.objects.filter(
            userid=user).exists()
        if session_exist:
            session = Sessions.objects.get(
                userid=user).status
            if session:
                username = UserCredentials.objects.get(userid=user).username
                rows = FuelQuotes.objects.filter(
                    userid=user).order_by("quoteid")
                data = []
                for row in rows:
                    quote = {'id': row.quoteid, "req_gallons": row.req_gallons,
                             "del_address":  row.del_address, "delivery_date":  row.delivery_date.strftime('%Y-%m-%d'), "sugg_price":  row.sugg_price, "due_amount": row.due_amount}
                    data.append(quote)

                if request.method == 'GET':
                    return render(request, 'fuel-quote-history.html', {'data': data, 'loginuser': username, 'history_active': True})
            else:
                return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
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


def suggested_price(request):
    if request.method == 'POST':
        gallon_req = int(request.POST['gallon_req'])
        if gallon_req > 0:
            user = int(request.session['id'])
            pricing = Pricing()
            sugg_price = pricing.get_suggested_price(user, gallon_req)
            sugg_price = round(sugg_price, 4)
            amount_due = round((sugg_price * gallon_req), 4)
            return JsonResponse({'status': 'ok', 'sugg_price': sugg_price, 'amount_due': amount_due})
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid Request'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid Request'})
