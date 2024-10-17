
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import connection

# Create your views here.
def index(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    x = category.objects.all().order_by('-id')[0:6]
    pdata = myproduct.objects.all().order_by('-id')[0:7]
    mydict = {"data": x, "prodata": pdata,"cart":ct}

    return render(request, 'user/index.html', context=mydict,)


###################################################
def about(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request, 'user/aboutus.html',{"cart":ct})


###################################################
def product(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request, 'user/product.html',{"cart":ct})


###################################################
def myorder(request):
    user = request.session.get('userid')
    oid=request.GET.get('oid')
    ct = ""
    mydict={}
    if user:
        if oid is not None:
            morder.objects.all().filter(id=oid).delete()
            return HttpResponse("<script>alert('Your Order has been Cancelled..');location.href='/user/myorder/'</script>")
        ct = mcart.objects.all().filter(userid=user).count()
        cursor=connection.cursor()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='"+str(user)+"' and o.remarks='Pending'")
        pdata=cursor.fetchall()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='" + str(user) + "' and o.remarks='Delivered'")
        ddata = cursor.fetchall()
        mydict={"pdata":pdata,"cart":ct,"ddata":ddata}
    return render(request, 'user/myorder.html',mydict)


###################################################
def enquiry(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.method == "POST":
        a = request.POST.get('name')
        b = request.POST.get('mob')
        c = request.POST.get('email')
        d = request.POST.get('msg')
        contactus(Name=a, Mobile=b, Email=c, Message=d).save()

    return render(request, 'user/enquiry.html',{"cart":ct})


###################################################
def signup(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Mobile = request.POST.get('mobile')
        Password = request.POST.get('passwd')
        Address = request.POST.get('address')
        Picture = request.FILES.get('ppic')
        x = register.objects.all().filter(email=Email).count()
        if x == 0:
            register(name=Name, mobile=Mobile, email=Email, passwd=Password, address=Address, ppic=Picture).save()
            return HttpResponse(
                "<script>alert('You are registered successfully..'); location.href='/user/signup/'</script>")
        else:
            return HttpResponse(
                "<script>alert('Your email id is already registered..'); location.href='/user/signup/'</script>")
    return render(request, 'user/signup.html',{"cart":ct})


###################################################
def myprofile(request):
    user=request.session.get('userid')
    x=""
    if user:
        if request.method=="POST":
            Name = request.POST.get('name')
            Mobile = request.POST.get('mobile')
            Password = request.POST.get('passwd')
            Address = request.POST.get('address')
            Picture = request.FILES.get('ppic')
            register(email=user,name=Name,mobile=Mobile,ppic=Picture,passwd=Password,address=Address).save()
            return HttpResponse("<script>alert('Your profile Updated Successfully...');location.href='/user/profile/'</script>")
        x=register.objects.all().filter(email=user)

    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    d = {"mydata": x,"cart":ct}
    return render(request, 'user/myprofile.html',d)


###################################################
def signin(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.method == "POST":
        Email = request.POST.get('email')
        Passwd = request.POST.get('passwd')
        x = register.objects.all().filter(email=Email, passwd=Passwd).count()
        y = register.objects.all().filter(email=Email,passwd=Passwd)
        if x == 1:
            request.session['userid'] = Email
            request.session['userpic']=str(y[0].ppic)
            return HttpResponse("<script>alert('You are login Successfully...');location.href='/user/index/'</script>")
        else:
            return HttpResponse(
                "<script>alert('Your userid or password is incorrect...');location.href='/user/signin/'</script>")

    return render(request, 'user/signin.html',{"cart":ct})


###################################################

def mens(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=1)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=1, pcategory=cid)
    mydict = {"cats": cat, 'data': d, "a": cid,"cart":ct}

    return render(request, 'user/mens.html', mydict,)


###################################################
def womens(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=2)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=2, pcategory=cid)
    mydict = {"cats": cat, 'data': d, "a": cid,"cart":ct}

    return render(request, 'user/womens.html', mydict)


###################################################
def kids(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=3)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=3, pcategory=cid)
    mydict = {"cats": cat, 'data': d, "a": cid,"cart":ct}

    return render(request, 'user/kids.html', mydict)


###################################################

def viewproduct(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    a = request.GET.get('msg')
    x = myproduct.objects.all().filter(id=a)
    return render(request, 'user/viewproduct.html', {"pdata": x, "msg": a,"cart":ct})


###########################################################
def signout(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.session.get('userid'):
        del request.session['userid']
    return HttpResponse("<script>alert('You are signout...');location.href='/user/index'</script>")


##################################################################################################
def myordr(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    user = request.session.get('userid')
    if user:
        pid = request.GET.get('msg')
        if pid is not None:
            morder(userid=user, pid=pid, remarks="Pending", odate=datetime.now().date(), status=True).save()
            return HttpResponse(
                "<script>alert('Your Order is Confirmed...');location.href='/user/index/'</script>")
    else:
        return HttpResponse("<script>alert('You have to login first...');location.href='/user/signin/'</script>")
    return render(request,{"cart":ct})

#########################################################################################################
def mycart(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    p=request.GET.get('pid')
    user=request.session.get('userid')
    if user:
        if p is not None:
            mcart(userid=user,pid=p,cdate=datetime.now().date(),status=True).save()
            return HttpResponse("<script>alert('Your Item is added in cart...');location.href='/user/viewproduct/'</script>")
    else:
        return HttpResponse("<script>alert('You have to login first...');location.href='/user/signin/'</script>")

    return render(request,'user/mcart.html',{"cart":ct})


def showcart(request):
    user=request.session.get('userid')
    md={}
    a = request.GET.get('msg')
    cid = request.GET.get('cid')
    pid = request.GET.get('pid')
    if user:
        if a is not None:
            mcart.objects.all().filter(id=a).delete()
            return HttpResponse("<script>alert('Your item is deleted from cart..');location.href='/user/showcart/'</script>")
        elif pid is not None:
            mcart.objects.all().filter(id=cid).delete()
            morder(userid=user,pid=pid,remarks="Pending",status=True,odate=datetime.now().date()).save()
            return HttpResponse("<script>alert('Your Order has been placed successfully..');location.href='/user/myorder/'</script>")

        cursor=connection.cursor()
        cursor.execute("select p.*,c.* from user_myproduct p,user_mcart c where p.id=c.pid and c.userid='"+str(user)+"'")
        cdata=cursor.fetchall()
        md={"cdata":cdata}


    return render(request,'user/showcart.html',md)



def cpdetail(request):
    c=request.GET.get('cid')
    p=myproduct.objects.all().filter(pcategory=c)
    return render(request,'user/cpdetail.html',{"pdata":p})
