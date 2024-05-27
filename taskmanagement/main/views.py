from django.shortcuts import render,redirect
from .models import Task
from .models import Info
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
# Create your views here.
date1=datetime.datetime.now()
date = datetime.datetime.now().year
def index(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phoneno=request.POST['phoneno']
        message=request.POST['message']
        info=Info(name=name,email=email,phoneno=phoneno,message=message)
        info.save()
           # Prepare email content
        context = {
            'name': name,
            'email': email,
            'phone': phoneno,
            'message': message,
            'date1':date1,
        }        
        # Render HTML email content
        html_content = render_to_string('msg.html', context)
        
        # Create plain text version
        plain_content = strip_tags(html_content)

        # Create the email
        subject = "Thank You for Contacting Us!"
        from_email = 'kingstonboysagar@gmail.com'
        recipient_list = [email]

        # Use EmailMultiAlternatives to send multi-part email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_content,  # The plain text part
            from_email=from_email,
            to=recipient_list,
        )

        # Attach HTML content
        email.attach_alternative(html_content, "text/html")

        # Send the email
        email.send(fail_silently=False)

        # Show a success message to the user
        messages.success(request, f"Hi {name}, thanks for contacting us! Please check your email for confirmation.")
        return redirect(index)
    return render(request,'index.html',{'date':date,'date1':date1})


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@login_required(login_url='log_in')
def dashboard(request):
    return render(request,'dashboard.html')

@login_required(login_url='log_in')
def addTask(request):
    if request.method=='POST':
        title=request.POST['title']
        desc=request.POST['desc']
        status=request.POST['status']
        assigned_to=request.POST['assigned_to']
        deadline=request.POST['deadline']
        Task.objects.create(title=title,desc=desc,status=status,assigned_to=assigned_to,deadline=deadline)
        messages.success(request,'Task added successfully') 
        return redirect('addTask')   
    return render(request,'addtask.html')

@login_required(login_url='log_in')
def delete_data(request, id):
    data = Task.objects.get(id=id)
    data.isDelete = True
    data.save()
    messages.success(request, 'Task deleted successfully')
    return redirect('viewTask')

@login_required(login_url='log_in')
def update_data(request,id):
    data=Task.objects.get(id=id)
    if request.method=='POST':
        title=request.POST['title']
        desc=request.POST['desc']
        status=request.POST['status']
        assigned_to=request.POST['assigned_to']
        deadline=request.POST['deadline']
        task=Task.objects.get(id=id)
        task.title=title
        task.desc=desc
        task.status=status
        task.assigned_to=assigned_to
        task.deadline=deadline
        task.save()
        messages.success(request,'successsfully updated')
        return redirect('addTask')
    return render(request,'update.html',{'data':data})


@login_required(login_url='log_in')
def viewTask(request):
    data = Task.objects.filter(isDelete=False)
    # Filter tasks based on status if status filter is provided
    status_filter = request.GET.get('status_filter')
    if status_filter:
        data = data.filter(status=status_filter)

    # Sort tasks based on sort_by parameter if provided
    sort_by = request.GET.get('sort_by')
    if sort_by:
        data = data.order_by(sort_by)

    return render(request, 'viewTask.html', {'data': data})

def register(request):
    if request.method=='POST':
        name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,f"Hello {name} your username is already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,f"Hello {name} your email is already exists!!")
                return redirect("register")
            else:
                User.objects.create_user(first_name=name,username=username,email=email,password=password)
                messages.success(request,f" Hello {name} you have register successfully")
        else:
            messages.error(request,"password doesn't match!!")
    return render(request,'auth/register.html')


def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not found")
            return redirect('log_in')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')    
    return render(request,'auth/login.html')


@login_required(login_url='log_in')
def  log_out(request):
    logout(request)
    return redirect('index')


# admin username:sagarthapa
# admin password:sagar123
