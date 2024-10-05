from .models import AddFlight,Passenger,PayModel
from django.shortcuts import redirect, render,get_object_or_404,HttpResponseRedirect, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from .forms import PassForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .forms import CodeForm

from .models import CustomUser
User = CustomUser

# Create your views here.

def book(request):
    list_val = AddFlight.objects.all()
    fl_num=0
    if request.method=='POST':
        from_city=request.POST['from']
        to=request.POST['to']
        print(from_city,to)
        from_add= AddFlight.objects.filter(From=from_city)
        to_add=AddFlight.objects.filter(To=to)
        f1=bool(AddFlight.objects.filter(From=from_city).exists())
        f2=bool(AddFlight.objects.filter(To=to).exists())
        if(from_city != to and f2==True and f1==True ):
            if( len(from_add) == len(to_add)):
                # fl_num=AddFlight.objects.only('number').get(From=from_city).id
                # # fl_details= AddFlight.objects.get(id=fl_num)
                # # print(len(fl_details))
                fl_num=len(from_add)
                return render(request,'v1/book.html',{'fl_num':fl_num,'list_val': list_val ,'from_city':from_city,'to':to})
        elif(from_city == to):
            messages.add_message(request,messages.ERROR,"Select Properly")
            return redirect('/')
        else:
            messages.add_message(request,messages.ERROR,"No Flights Available")
            return redirect('/')
    context = {'list_val': list_val,'fl_num':fl_num }
    return render(request,'v1/book.html',context)

def home(request):
    return render(request,'v1/home.html')

def booking(request,id):
    fl_det = AddFlight.objects.filter(id=id)
    question = get_object_or_404(AddFlight, pk=id)
    pass_det_fin=Passenger.objects.filter(fl_details=question) & Passenger.objects.filter(user=request.user)
    count=len(pass_det_fin)
    if request.method =='POST':
        form = PassForm(request.POST)
        if form.is_valid():
            user=request.user
            fl_details= AddFlight.objects.get(id=id)
            Pass_name=form.cleaned_data['Pass_name']
            age=form.cleaned_data['age']
            gender=form.cleaned_data['gender'] 
            Pass = Passenger(Pass_name=Pass_name,age=age,gender=gender,user=user,fl_details=fl_details)
            if request.POST['submit']=='add':
                    Pass.save()
                    form = PassForm() 
                    print('Entry Succesfull')
            else:
                    print(request.POST['submit'])
                    id=request.POST['submit']
                    pass_det_fin=Passenger.objects.filter(fl_details=question) & Passenger.objects.filter(user=request.user) & Passenger.objects.filter(id=id)
                    pass_det_fin.delete()
                    print('Deleted Succesfull')
            form = PassForm() 
            return redirect(request.META['HTTP_REFERER'])    
    else:
        print('not valid')
        form = PassForm()
        context = {'fl_det': fl_det,'form':form,'pass_det_fin':pass_det_fin,'count':count}
        return render(request,'v1/booking.html',context)

        # return redirect(request.META['HTTP_REFERER'])
    context = {'fl_det': fl_det,'form':form,'pass_det_fin':pass_det_fin,'count':count}
    return render(request,'v1/booking.html',context)

def Pay(request):
    if request.method=='POST':
        card_name=request.POST['card_name']
        card_num=request.POST['card_num']
        expiry_month=request.POST['expiry_month']
        expiry_year=request.POST['expiry_year']
        cvv_num=request.POST['cvv_num']
        fl_det=int(request.POST['fl_det'])

        # status=request.POST['status']
        # passenger=  Passenger.objects.get()

        print(fl_det)
        fl_num = get_object_or_404(AddFlight, pk=fl_det)
        pay=PayModel.objects.create(user=request.user,fl_det=fl_num,card_name=card_name,card_num=card_num,expiry_month=expiry_month,expiry_year=expiry_year,cvv_num=cvv_num)
        print("payment successful ")
        pay.save()

        fl_details=AddFlight.objects.all().filter(id=fl_det)
        pass_det_fin=Passenger.objects.filter(fl_details=fl_det) & Passenger.objects.filter(user=request.user)
 

        #seat numbers
        pass_det_fin=Passenger.objects.filter(fl_details=fl_det) & Passenger.objects.filter(user=request.user)
        number_fl = str(get_object_or_404(AddFlight, pk=fl_det))
        number=number_fl[:2]
        ticket=[]
        count=1
        for i in range(len(pass_det_fin)):
            ticket.append(number+str(count))
            count=count+1
        print(ticket)

        #passenger list for ticket
        fl_class=AddFlight.objects.only('class_type').filter(id=fl_det)
        print(fl_class)
        len_passenger=len(pass_det_fin)
        print(len_passenger)
        print(pass_det_fin)

        #zipping the passenger and ticket list
        zip_list=zip(ticket,pass_det_fin)
        pass_list_ticket=list(zip_list)

        context={'fl_details':fl_details,'pass_det_fin':pass_det_fin,'ticket':ticket,'len_passenger':len_passenger,'pass_list_ticket':pass_list_ticket}
        return render(request,'v1/ticket.html',context)
    else:
        print("payment not succesful")
        return render(request,'v1/booking.html')

def login(request):
    # if request.method =='POST':
    #     username=request.POST['uname']
    #     password=request.POST['password']

    #     try:
    #         user = authenticate(username=User.objects.get(email=username),password=password)
    #     except:
    #         user = authenticate(username=username,password=password)
    #     # check_user=User.objects.filter(username=username,password=password)
    #     if user is not None and ( User.objects.filter(username=username) | User.objects.filter(email=username)):
    #         request.session['user']=username
    #         auth_login(request,user)
    #         messages.add_message(request,messages.SUCCESS,"You have Loggined in Successfully")
    #         request.session['pk'] = user.pk
    #         print('Logged in')
    #         return redirect('verify-view')
    #     elif(bool(User.objects.filter(username=username) | User.objects.filter(email=username))==False):
    #         messages.add_message(request,messages.SUCCESS,"Please Register to Book")
    #         return redirect("login")
    #     else:
    #         messages.add_message(request,messages.ERROR,"Check Your Details")
    #         print('Not Logged in')
    # return render(request,'v1/login.html')

    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('uname')
        #print(username)
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            request.session['user']=username
            auth_login(request, user)
            messages.add_message(request,messages.SUCCESS,"You have Loggined in Successfully")
            request.session['pk'] = user.pk
            return redirect('verify-view')
    return render(request, 'v1/login.html',{'form': form})

def register(request):
    if request.method =='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=uname).exists():
                messages.add_message(request,messages.ERROR,"Username Taken ")
                print('Username taken')
            elif User.objects.filter(email=email).exists():
                messages.add_message(request,messages.ERROR,"Email already Exists")
                print('Email taken')
            else:
                user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=password1)
                user.save()
                print('user created')
                messages.add_message(request,messages.SUCCESS,"Registred Succesfully,Login to Book the Ticket.")
                return redirect('login')
        else:
            print('password not matching')
            messages.add_message(request,messages.ERROR,"Password Not matching")

        return redirect('register')

    return render(request,'v1/signup.html')


def logout_user(request):
    try:
        del request.session['user']
        logout(request)
    except:
        logout(request)
        return redirect('/')
   
    return redirect('/')

def auth_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect(verify_view)
    return render(request, 'auth.html',{'form': form})
            
def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = CustomUser.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.username}: {user.code}"
        if not request.POST:
            print(code_user)
            # send SMS
        
        if form.is_valid():
            num = form.cleaned_data.get('number')
            print(num)
            if str(code) == str(num):
                print("SMS verification success")
                code.save()
                login(request)
                return redirect('home')
            else:
                return redirect('login')
    return render(request, 'v1/verify.html', {'form':form})
