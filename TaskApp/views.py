from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import TaskTable
import json
import datetime

@login_required
def dashboard(request):
    if request.user.is_superuser:
        today = datetime.date.today()
        if request.method == 'POST':
            if 'date_form' in request.POST:
                selected_date = request.POST.get('date') 
                normal_users = User.objects.filter(is_superuser=False) 
                developers = []
                for user in normal_users:
                    tasks_for_selected_date = user.task_set.filter(date=selected_date)
                    number_of_tasks = tasks_for_selected_date.first().number_of_tasks if tasks_for_selected_date else '---'  # Set to '-' if no tasks for the selected date
                    remarks = tasks_for_selected_date.first().remarks if tasks_for_selected_date else '---'  # Set to '-' if no tasks for the selected date
                    no_of_complete=tasks_for_selected_date.first().no_of_complete if tasks_for_selected_date else '---'
                    developers.append({
                    'date': selected_date,
                    'user': user,
                    'number_of_tasks': number_of_tasks,
                    'no_of_complete': no_of_complete,
                    'remarks': remarks,
                    })
                
                return render(request, 'superuser_page.html',{'developers':developers})
        else:
            return render(request, 'superuser_page.html',{'developers':{}})

    else:
        def condRender():
            context={'added':0}
            today = datetime.date.today()
            tast = TaskTable.objects.filter(date=today,user=request.user)
            if tast.exists():
                context['assign']=tast
                context['added']=1
                for task in tast:
                    if task.no_of_complete==task.number_of_tasks:
                        context['added']=2
                
            return context
        
        if request.method=='POST':
            data = json.loads(request.POST['tasksObject'])
            today = datetime.date.today()
            if data['form_type']=='task_form':
                tasks=data['Tasks']
                tk = TaskTable.objects.create(user=request.user, date=today, task_array=tasks, number_of_tasks=len(tasks), remarks='',no_of_complete=0)
                tk.save() 
                
                return render(request, 'user_page.html',condRender())
            elif data['form_type']=='remarks_form':
                remarks=data['Remarks']
                check_data=data['check']
                number_of_completed=data['completed']
                tat = TaskTable.objects.filter(date=today,user=request.user)
                obj = tat.get()
                if obj and obj.number_of_tasks != 0:
                    task_data = TaskTable.objects.get(user=request.user,date=today)
                    task_data.no_of_complete=number_of_completed
                    task_data.remarks = remarks
                    for t, c in zip(task_data.task_array, check_data):
                        t['isChecked'] = c['isc']
                    task_data.save()

                return render(request, 'user_page.html',condRender())
           
        
        return render(request, 'user_page.html',condRender())
 

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
                    messages.warning(request, 'Email already exists.')
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