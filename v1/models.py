from django.db import models


# Create your models here.
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length = 12)

class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_item = []

        for i in range(5):
            num = random.choice(number_list)
            code_item.append(num)

        code_string = "".join(str(item) for item in code_item)
        self.number = code_string
        print(self.number)
        super().save(*args, **kwargs)

class AddFlight(models.Model):
    CLASS_CHOICES =(
    ("Economy Class", "Economy Class"),
    ("Business Class", "Business Class"),
    ("First class", "First Class"),)   
    airlines=models.CharField(max_length=20)
    number=models.CharField(max_length=10)
    From=models.CharField(max_length=10)
    To=models.CharField(max_length=10)
    Date=models.DateField(max_length=10)
    Time=models.TimeField(max_length=10)
    Price=models.FloatField(max_length=10)
    class_type=models.CharField(max_length=20,choices = CLASS_CHOICES)


    def __str__(self):
        return self.number

class Passenger(models.Model):
    GENDER_CHOICES = (
   ('Male', 'Male'),
   ('Female', 'Female'))
    user=models.ForeignKey(CustomUser,on_delete=CASCADE)
    fl_details=models.ForeignKey( AddFlight,related_name='fl_det',on_delete=CASCADE)
    Pass_name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(choices=GENDER_CHOICES,max_length=50)
    book_time_date=models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(blank=True,null=True)


class PayModel(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=CASCADE)
    fl_det=models.ForeignKey(AddFlight,on_delete=CASCADE,blank=True,null=True)
    card_name=models.CharField(max_length=100)
    card_num=models.CharField(max_length=100)
    expiry_month=models.IntegerField()
    expiry_year=models.IntegerField()
    cvv_num=models.IntegerField()
    
