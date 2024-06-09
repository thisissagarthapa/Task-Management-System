from django.shortcuts import render, redirect
from .models import Task, Info
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
import datetime

current_date = datetime.datetime.now()
current_year = datetime.datetime.now().year

def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phoneno = request.POST['phoneno']
        message = request.POST['message']
        info = Info(name=name, email=email, phoneno=phoneno, message=message)
        info.save()

        # Prepare email content
        context = {
            'name': name,
            'email': email,
            'phone': phoneno,
            'message': message,
            'date1': current_date,
        }

        # Render HTML email content
        html_content = render_to_string('msg.html', context)
        plain_content = strip_tags(html_content)

        # Create the email
        subject = "Thank You for Contacting Us!"
        from_email = 'kingstonboysagar@gmail.com'
        recipient_list = [email]

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_content,
            from_email=from_email,
            to=recipient_list,
        )

        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        messages.success(request, f"Hi {name}, thanks for contacting us! Please check your email for confirmation.")
        return redirect('index')

    return render(request, 'index.html', {'date': current_year, 'date1': current_date})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='log_in')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='log_in')
def addTask(request):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        status = request.POST['status']
        assigned_to = request.POST['assigned_to']
        deadline = request.POST['deadline']
        Task.objects.create(title=title, desc=desc, status=status, assigned_to=assigned_to, deadline=deadline)
        messages.success(request, 'Task added successfully')
        return redirect('addTask')
    return render(request, 'addtask.html')


@login_required(login_url='log_in')
def delete_data(request, id):
    data = Task.objects.get(id=id)
    data.isDelete = True
    data.save()
    messages.success(request, 'Task deleted successfully')
    return redirect('viewTask')


@login_required(login_url='log_in')
def update_data(request, id):
    data = Task.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        status = request.POST['status']
        assigned_to = request.POST['assigned_to']
        deadline = request.POST['deadline']
        task = Task.objects.get(id=id)
        task.title = title
        task.desc = desc
        task.status = status
        task.assigned_to = assigned_to
        task.deadline = deadline
        task.save()
        messages.success(request, 'Successfully updated')
        return redirect('addTask')
    return render(request, 'update.html', {'data': data})


@login_required(login_url='log_in')
def viewTask(request):
    data = Task.objects.filter(isDelete=False)

    status_filter = request.GET.get('status_filter')
    if status_filter:
        data = data.filter(status=status_filter)

    sort_by = request.GET.get('sort_by')
    if sort_by:
        data = data.order_by(sort_by)

    return render(request, 'viewTask.html', {'data': data})


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, f"Hello {name}, your username already exists.")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, f"Hello {name}, your email already exists.")
                return redirect('register')
            else:
                User.objects.create_user(first_name=name, username=username, email=email, password=password)
                messages.success(request, f"Hello {name}, you have registered successfully.")
                return redirect('log_in')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'auth/register.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username not found.")
            return redirect('log_in')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'auth/login.html')


@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('index')


@login_required(login_url='log_in')
def task_report(request):
    tasks = Task.objects.filter(isDelete=False)

    # Calculate tasks per status
    tasks_per_status = tasks.values('status').annotate(total=Count('status'))

    # Calculate tasks per user
    tasks_per_user = tasks.values('assigned_to').annotate(total=Count('assigned_to'))

    # Calculate total, completed, in progress, and open tasks
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    inprogress_tasks = tasks.filter(status='inprogress').count()
    open_tasks = tasks.filter(status='open').count()

    context = {
        'tasks_per_status': list(tasks_per_status),
        'tasks_per_user': list(tasks_per_user),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'inprogress_tasks': inprogress_tasks,
        'open_tasks': open_tasks,
        'date1': datetime.date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'report.html', context)
