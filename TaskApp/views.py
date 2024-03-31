from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import TaskTable,RemarksTable,User
import json
import datetime
from django.http import HttpResponseForbidden


@login_required
def dashboard(request):
    if request.user.is_superuser:
  
        if request.method == 'POST':
            if 'date_form' in request.POST:
                selected_date = request.POST.get('date') 
                normal_users = User.objects.filter(is_superuser=False) 
                developers = []
                for user in normal_users:
                    tasks = TaskTable.objects.filter(user=user, date=selected_date)
                    remarks = RemarksTable.objects.filter(user=user, date=selected_date)
                    number_of_tasks = tasks.count()
                    no_of_complete = tasks.filter(is_checked=True).count()
                    developers.append({
                        'date': selected_date,
                        'user': user,
                        'number_of_tasks': number_of_tasks,
                        'no_of_complete': no_of_complete,
                        'remarks': remarks,
                        'task_array': tasks,
                    })
                    # ct_count = tasks.filter(is_checked=True).count()
                    # context[user.username]=({'date': selected_date, 'tasks': tasks, 'remarks': remarks ,'total':t_count,'copleted':ct_count})
                context = {
            'developers': developers,
        }

                print(context)
                return render(request, 'superuser_page.html',context)
        else:
            return render(request, 'superuser_page.html')

    else:
        def condRender():
            context={}
            today_date = datetime.date.today()
            tasks = TaskTable.objects.filter(date=today_date,user=request.user)
            if tasks.exists():
                context['assign']=tasks
                context['total_tasks'] = tasks.count()
                context['completed_tasks'] = tasks.filter(is_checked=True).count()
            return context
        
        if request.method=='POST':
            data = json.loads(request.POST['tasksObject'])
            if data['form_type']=='task_form':
                tk = TaskTable.objects.create(
                    user=request.user,
                    taskName=data['taskName'],
                    taskTime=data['taskTime'],
                    taskType=data['taskType'],
                    created_at=datetime.datetime.now(),
                    )
                tk.save()
                return render(request, 'user_page.html',condRender())
            
            elif data['form_type']=='remarks_form':
                today_date = datetime.date.today()
                remarks=data['Remarks']
                check_data=data['check']
                task_data = TaskTable.objects.filter(date=today_date,user=request.user)
                for t, c in zip(task_data, check_data):
                    if c['isc']==True:
                        t.is_checked = c['isc']
                        if t.completed_at==None:
                            t.completed_at=datetime.datetime.now()
                        t.save()
                    else:
                        t.is_checked = c['isc']
                        t.completed_at=None;
                        t.save()
                rt = RemarksTable.objects.filter(date=today_date,user=request.user)
                if rt.exists():
                    obj=rt.first()
                    obj.remarks=remarks
                    obj.save()
                else:
                    crt = RemarksTable.objects.create(
                    user=request.user,
                    remarks=remarks
                    )
                    crt.save()
        return render(request, 'user_page.html',condRender())
 

def loginPage(request):
    if request.method=='POST':
        email=request.POST.get('mail')
        password=request.POST.get('password')
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

@login_required
def devmanage(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
 
    if request.method == 'POST':
        form_type = request.POST.get('form_type', None)
        if form_type == 'add_form':
            # Process add user form
            email = request.POST.get('email')
            password = request.POST.get('password')
            if email and password:  # Check if email and password are provided
                try:
                    myuser = User.objects.create_user(email, email, password)
                    messages.success(request, f"User {email} added successfully.")
                except Exception as e:
                    messages.error(request, f"Failed to add user: {e}")
            else:
                messages.error(request, "Email and password are required.")
            return redirect('devmanagement')  
        elif form_type == 'delete_form':
            email_to_delete = request.POST.get('email')
            try:
                user_to_delete = User.objects.get(email=email_to_delete)
                user_to_delete.delete()
                messages.success(request, f"User {email_to_delete} deleted successfully.")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
            return redirect('devmanagement')  
    
    
    return render(request, 'devmanage.html')