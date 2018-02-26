from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.urlresolvers import reverse

# import bcrypt
# Create your views here.
def index(request):
    return render(request, 'logRegApp/index.html')
    pass

def r_process(request):
    data ={
        "name":request.POST['name'],
        "usern":request.POST['usern'],
        "pass":request.POST['pass'],
        "cpass":request.POST['cpass']
    }
    result = User.objects.validate(data)
    print"^"*25
    print data
    print"^"*25

    if result[0]:
        request.session['userInfo']=result[1].id
        return redirect("/success")
    else:
        for errors in result[1]:
            messages.error(request, errors)
        return redirect("/")


def l_process(request):
    data = {
    'username':request.POST['usern'],
    'pass':request.POST['pass'],
    }
    print data
    result = User.objects.l_process(data)
    print result

    if result[0]:
        request.session['userInfo']=result[1].id
        print"$--request"*30
        return redirect(reverse ('travel:index'))
    else:
        for errors in result[1]:
            messages.error(request, errors)
        return redirect("/")
    # request.session.clear()

def success(request):
    try:
        user_obj = User.objects.get(id=request.session['userInfo'])
        context = {"user": user_obj}
        return render(request, "success.html", context)
    except:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")
