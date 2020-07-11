from django.db import models
from django.core.validators import MinLengthValidator


class UserCredentials(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(
        validators=[MinLengthValidator(6)], max_length=20)
    confirm_password = models.CharField(
        validators=[MinLengthValidator(6)], max_length=20)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return self.username


class States(models.Model):
    stateid = models.AutoField(primary_key=True)
    code = models.CharField(validators=[MinLengthValidator(2)], max_length=2)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['-code']


class ClientInformations(models.Model):
    userid = models.OneToOneField(
        UserCredentials, on_delete=models.CASCADE, primary_key=True)
    fullname = models.CharField(
        validators=[MinLengthValidator(1)], max_length=50)
    address1 = models.CharField(
        validators=[MinLengthValidator(1)], max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(validators=[MinLengthValidator(1)], max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(
        validators=[MinLengthValidator(5)], max_length=9)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return self.fullname


class FuelQuotes(models.Model):
    quoteid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(
        UserCredentials, on_delete=models.CASCADE)
    req_gallons = models.IntegerField()
    del_address = models.CharField(max_length=100)
    delivery_date = models.DateTimeField(auto_now=False)
    sugg_price = models.DecimalField(max_digits=9, decimal_places=3)
    due_amount = models.DecimalField(max_digits=9, decimal_places=3)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ['-created_on']


class Sessions(models.Model):
    userid = models.IntegerField(unique=True)
    status = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
