from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.urls import reverse
import uuid
from django.conf import settings
# Create your views here.


COOKIE_ID = 'todo_user_id'     
COOKIE_NAME = 'todo_user_name' 
COOKIE_SALT = 'todo-app'
COOKIE_AGE = 60 * 60 * 24 * 365

# rendering active tasks
def home(request):
    try:
        owner_id_str = request.get_signed_cookie(COOKIE_ID, salt=COOKIE_SALT)
        owner_uuid = uuid.UUID(owner_id_str)
        owner_name = request.get_signed_cookie(COOKIE_NAME, salt=COOKIE_SALT)
    except Exception:    
        return redirect('landingPage')
    tasks=Tasks.objects.filter(task_status=True,owner_id=owner_uuid)
    return render(request,'home.html',{'tasks':tasks,'user_name':owner_name})

# creating new taks
def createTask(request):
    try:
        owner_name=request.get_signed_cookie(COOKIE_NAME,salt=COOKIE_SALT)
        owner_id_str = request.get_signed_cookie(COOKIE_ID, salt=COOKIE_SALT)
        owner_uuid = uuid.UUID(owner_id_str)
    except Exception:
        return redirect('landingPage')
    if request.method=="POST":
        task=request.POST.get('task-name','').strip()
        if task:
            Tasks.objects.create(
                task_name=task,
                owner_id=owner_uuid,
                user_name=owner_name
            )
        return redirect("home")

# rendering completed tasks
def completedTasks(request):
    try:
        owner_id_str = request.get_signed_cookie(COOKIE_ID, salt=COOKIE_SALT)
        owner_uuid = uuid.UUID(owner_id_str)
        owner_name = request.get_signed_cookie(COOKIE_NAME, salt=COOKIE_SALT)

    except Exception:
        return redirect('landingPage')
    tasks=Tasks.objects.filter(task_status=False,owner_id=owner_uuid)
    return render(request,'completed.html',{'tasks':tasks,'user_name':owner_name})


# marking task status
def markTask(request,task_id):
    task_to_mark=get_object_or_404(Tasks,id=task_id)
    curr_status=task_to_mark.task_status
    task_to_mark.task_status=not curr_status
    task_to_mark.save()
    next_url = request.GET.get('next')
    if not next_url:
        next_url = request.META.get('HTTP_REFERER')
    if not next_url:
        next_url = reverse('home')
    return redirect(next_url)
    return redirect('home')

# delete tasks
def deleteTask(request,task_id):
    task_to_del=get_object_or_404(Tasks,id=task_id)
    task_to_del.delete()
    next_url = request.GET.get('next')
    if not next_url:
        next_url = request.META.get('HTTP_REFERER')
    if not next_url:
        next_url = reverse('home')
    return redirect(next_url)

#all tasks
def renderTasks(request):
    try:
        owner_id_str = request.get_signed_cookie(COOKIE_ID, salt=COOKIE_SALT)
        owner_uuid = uuid.UUID(owner_id_str)
        owner_name = request.get_signed_cookie(COOKIE_NAME, salt=COOKIE_SALT)
    except Exception:
        return redirect('landingPage')
    tasks=Tasks.objects.filter(owner_id=owner_uuid).order_by('-task_status','created_at')
    return render(request,'allTasks.html',{'tasks':tasks,'user_name':owner_name})

# landingpage
def landingPage(request):
    if 'todo_user_id' in request.COOKIES:
        return redirect('home')
    if request.method=="POST":
        user_name=request.POST.get('username','').strip()
        if not user_name:
            return render(request,'landingPage.html',{'error':'please enter name to proceed'})
        unique_id=uuid.uuid4()
        resp=redirect('home')
        resp.set_signed_cookie(
            COOKIE_ID,
            str(unique_id),
            salt=COOKIE_SALT,
            max_age=COOKIE_AGE,
            httponly=True,
            secure=not settings.DEBUG
        )
        resp.set_signed_cookie(
            COOKIE_NAME,
            user_name,
            salt=COOKIE_SALT,
            max_age=COOKIE_AGE,
            httponly=False,
            secure=not settings.DEBUG
        )
        return resp
    
    return render(request,'landingPage.html')

        
def custom_404(request):
    return render(request,'404.html')
