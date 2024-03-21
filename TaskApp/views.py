from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from .models import TaskTable
import json
import datetime

@login_required
def dashboard(request):


    if request.user.is_superuser:
        # Render template for superuser
        today = datetime.date.today()
        
        a=True
        
        if request.method == 'POST':
            if 'assign_form' in request.POST:
                regular_users = User.objects.filter(is_superuser=False)
                
                for user in regular_users:
                    task_data = TaskTable.objects.create(user=user, date=today, task_array=[], number_of_tasks=0, remarks='',no_of_complete=0)
                    task_data.save() 
                a=False
                return render(request, 'superuser_page.html',{'developers':{},'a':a})
            elif 'date_form' in request.POST:
                selected_date = request.POST.get('date')  
                ta = TaskTable.objects.filter(date=today)
                if ta.exists():
                    a=False
                print(selected_date)
                tasks = TaskTable.objects.filter(date=selected_date)

                for task in tasks:
                   print("Developers are printed in table", task)
                
                return render(request, 'superuser_page.html',{'developers':tasks,'a':a})
        else:
            # here the date filter should be passed
            return render(request, 'superuser_page.html',{'developers':{},'a':a})


    













    else:
        

        today = datetime.date.today()
        tast = TaskTable.objects.filter(date=today,user=request.user)
        if request.method=='POST':
            data = json.loads(request.POST['tasksObject'])
            if data['form_type']=='task_form':
                tasks=data['Tasks']
                #date=data['Date']
                #remarks=data['Remarks']
                tat = TaskTable.objects.filter(date=today,user=request.user)
                obj = tat.get()
                if obj and obj.number_of_tasks == 0:
                    task_data = TaskTable.objects.get(user=request.user,date=today)
                    task_data.task_array = tasks
                    task_data.number_of_tasks = len(tasks)
                    #task_data.remarks = remarks
                    task_data.save()

                return render(request, 'user_page.html',{'assign':tat})
            

            elif data['form_type']=='remarks_form':
                #tasks=data['Tasks']
                #date=data['Date']
                print('VAndichu')
                remarks=data['Remarks']
                number_of_completed=data['completed']
                print(remarks)
                tat = TaskTable.objects.filter(date=today,user=request.user)
                obj = tat.get()
                if obj and obj.number_of_tasks != 0:
                    task_data = TaskTable.objects.get(user=request.user,date=today)
                    #task_data.task_array = tasks
                    #task_data.number_of_tasks = len(tasks)
                    task_data.no_of_complete=number_of_completed
                    task_data.remarks = remarks
                    task_data.save()

                return render(request, 'user_page.html',{'assign':tat})
           
        
        return render(request, 'user_page.html',{'assign':tast})
    














    
    

def loginPage(request):
    if request.method=='POST':
        email=request.POST.get('mail')
        password=request.POST.get('password')
        print(email,password)
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,'Wrong Credentials')
            return redirect('loginPage')

    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('loginPage')


def registerPage(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('password')
        conf_password = request.POST.get('password2')
        if password == conf_password:
            if email.endswith('@cyces.co'):
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'Email already exists. Please use a different email.')
                    return redirect('registerPage')  
                else:
                    myuser = User.objects.create_user(email, email, password)
                    messages.success(request, 'User created successfully. You can now login.')
                    return redirect('loginPage') 
            else:
                messages.error(request, 'Email must end with cyces.co.')
                return redirect('registerPage') 
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('registerPage') 

    return render(request, 'register.html')

def notfound(req):
    return render(req,'404.html')