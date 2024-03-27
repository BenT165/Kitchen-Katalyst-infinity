from django.contrib.auth.models import UserManager #we are overriding UserManager class
from django.db import models
from django.utils import timezone


class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=30, blank=False)
    userID = models.AutoField(primary_key=True)
    date_reminder = models.IntegerField(default='1')
    last_login = models.DateTimeField(default=timezone.now)

    #security_question = models.OneToOneField('Security_Question', on_delete=models.CASCADE)
    #security_question_answer = models.CharField(max_length=100)
    

    def check_password(self, password):
        return self.password == password

class Grocery(models.Model):
    groceryID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groceries')
    quantity = models.IntegerField()
    name = models.CharField(max_length=30, blank=False)
    unit = models.CharField(max_length=25, blank=True)
    expiration_date = models.DateField()
    custom_reminder = models.BooleanField(default='False') #date_reminder days before expiration_date
    is_expired = models.BooleanField(default='False') #on expiration_date
    day_before = models.BooleanField(default='False') #24 hours before item expires

    def __srt__(self):
        return self.quantity + ' ' + self.name + ' '  + self.expiration_date

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', default='1')
    name = models.CharField(max_length=50)
    instructions = models.TextField(max_length=1500)

class Security_Question(models.Model):
    questionID = models.IntegerField(primary_key=True)
    #question = models.CharField(max_length=100)
    
class Password_History(models.Model):
    password = models.CharField(max_length=50)
    passwordID = models.AutoField(primary_key=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_histories')


