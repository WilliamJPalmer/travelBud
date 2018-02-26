from django.shortcuts import render, redirect
from django.contrib import messages
from ..logRegApp.models import User
from django.core.urlresolvers import reverse
from .models import Trip
from django.db.models import Q

def index(request):

    result=User.objects.get(id=request.session['userInfo'])

    context = {
        'user': result.username,
        'planned_trips': Trip.objects.filter(Q(planner_id=request.session['userInfo']) | Q(joiners=request.session['userInfo'])),
        'trips':Trip.objects.all().exclude(Q(planner_id=request.session['userInfo']) | Q(joiners=request.session['userInfo']))

    }
    return render(request, 'travelBudApp/index.html', context)


def addTrip(request):
    return render(request, 'travelBudApp/addTrip.html')

def newTrip(request):
    print"&"*50
    data = {
    "destination":request.POST['destination'],
    "description":request.POST['description'],
    "travelStart":request.POST['travelStart'],
    "travelEnd":request.POST['travelEnd'],
    "planner_id":request.session['userInfo']
    }
    user = User.objects.get(id=request.session['userInfo'])
    print (user)
    print"$^^^^^^$XXXX"*7
    result = Trip.objects.verify(data)
    # this is where the path goes the the models.py file and goes through the verify function, def verify(self,data):

    # Once the logic is completed in the models.py file, the return will come back here and continue the code below.
    trips=Trip.objects.all()
    print trips
    print"$"*45
    # context = {
    #     'trips':trips
    # }
    if result[0]:
        print (result)
        print"!!!!^^^"*4
        return redirect(reverse('travel:index'))
    else:
        for errors in result[1]:
            messages.error(request, errors)
            print (errors)
            print"^^^^&&&"*10
        return redirect(reverse("travel:addTrip"))


def joinPlan(request, id):

    joining = User.objects.get(id=request.session['userInfo'])
    # joining is getting the id of the user that is logged in and is clicking on the join link of a trip.
    trip_joining = Trip.objects.get(id=id)
    # trip_joining is getting the id of the trip whose join link is being clicked.

    trip_joining.joiners.add(joining)
    # this is adding trip being joined(trip_joining), the joining user(joining) and then creating a new table. Each row in the new table will have a primary key, a trip_id and user_id. The trip_id is supplied by the trip_joining and the user_id ist supplied by the joining. Joiners is the name of the ManyToManyField in the Trip class. The new table will be the class name and the column head you join on. The table name for this join will be "trip_joiners", "trip" for the class and "joiners" for the ManyToManyField in that table.

    return redirect(reverse ('travel:index'))



def destDetail(request,id):
    trips = Trip.objects.get(id=id)

    context = {
    "trips":trips,
    "planner": User.objects.get(id=trips.planner_id),
    'joiningusers':trips.joiners.all(),
    }

    return render(request, 'travelBudApp/destination.html', context)
