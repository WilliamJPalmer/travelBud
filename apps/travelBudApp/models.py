from __future__ import unicode_literals
from ..logRegApp.models import User
from django.db import models
# from datetime import date
import datetime

# Create your models here.
class TripManager(models.Manager):
    def verify(self,data):#the data in the verify(self,data) is the dictionary that is in the views.py newTrip function. This contains the information that was entered on the Add Trip.html page and also will have the id of the user that is adding the trip.
        flag = True
        errors = []
        print"@@!"*10
        if len(data['destination']) < 1:
            flag = False
            errors.append("You must enter a destination.")
            print"@@!DEST"*10
            # return (False, errors)
        if len(data['description']) < 1:
            flag = False
            errors.append("You must enter a description.")
            print"@@!DESCRP"*10
            # return (False, errors)
        if data['travelStart'] == "":
            flag = False
            errors.append("You must enter a Start Date.")
            print"@@!TS"*10
            # return (False, errors)
        if data['travelEnd'] == "":
            flag = False
            errors.append("You must enter an End Date.")
            print"@@!TEND"*10
            # return (False, errors)
        if data['travelStart'] <= str(datetime.date.today()):
            flag = False
            errors.append("Time travel not possible yet. Choose a start date after today")
            print"@@!TravelEnd"*3
        if data['travelEnd'] <= data['travelStart']:
            flag = False
            errors.append("Time travel not possible yet. Make sure Start date is after today and End date is after Start date.")
            print"@@!TravelEndOverStart"*3
        if flag:
            # if flag: states that Flag=True or that Flag exists. this means that no errors were encoutered in the if statements above. Only if there were no errors would we be inside this if statement. The create statement below only happens if True has not been changed to False in the verify if statements.
            trip = Trip.objects.create(destination=data['destination'], description=data['description'],travel_start=data['travelStart'], travel_end=data["travelEnd"], planner_id=data['planner_id'])
            return (True, trip)
            # the return (True, trip) is returned so that when we go back to the views.py to finsh the logic in the newTrip route we can set conditions of what to do and where to go. In the case of the return (True, trip) above, when we go back to the views.py, the result will be true and the create statement will run and we will be directed to a destination, in this case it will be to the index page of the travel app. If errors are found in the verify function, the else statement below will run and be sent to the views.py file.
        else:
            return (False, errors)


class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    travel_start = models.DateField()
    travel_end= models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    joiners = models.ManyToManyField(User, related_name='join_user')
    planner = models.ForeignKey( User, related_name= 'plan_user')
    objects = TripManager()
