from __future__ import unicode_literals

from django.db import models
import bcrypt
from bcrypt import hashpw, gensalt
# Create your models here.

class UserManager(models.Manager):
    def validate(self, data):

        flag = True
        errors = []

        password=data['pass']
        hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

        print hashed
        print'!@$%&'*27

        if len(data['name']) < 3:
            flag = False
            errors.append("Name must be at least three characters long.")

        if len(data['usern']) < 3:
            flag = False
            errors.append("Username must be at least three characters long.")

        if data['pass'] != data['cpass']:
            flag = False
            errors.append('Passwords must match')

        if len(data['pass']) < 8:
            flag = False
            errors.append("Password must be at least 8 characters long")

        if flag:
            # hashed = bcrypt.hashpw(data['pass'].encode(), bcrypt.gensalt())
            user=User.objects.create(name=data['name'], username=data['usern'], password=hashed)

            return (True, user)
        else:
            return (False, errors)


    def l_process(self,data):
        flag = True
        errors = []
        suspect_user = User.objects.filter(username=data['username'])
        print"*++++==="*49
        print suspect_user
        if not suspect_user:
            flag = False
            errors.append('Invalid username')
            print"^^^^"*1
            return (False, errors)
        elif suspect_user:
            hashed = suspect_user[0].password
            hashed = hashed.encode('utf-8')
            print hashed
            password = str(data['pass'])
            print">>>>>>>8"*3
            if bcrypt.hashpw(password, hashed) == hashed:
                print hashed
                print"*!!!"*35
                print password
                print hashed
                # return (True, User.objects.filter())
                return (True, suspect_user[0])

            else:
                flag = False
                errors.append("Invalid password")
            return (False, errors)

        else:
            print"&----ELSE"*30

            return (True, suspect_user[0])

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
