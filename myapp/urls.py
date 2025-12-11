from django.urls import path
from .views import *

urlpatterns=[
    path('home/',home,name='home'),
    path('completedTasks/',completedTasks,name='completedTasks'),
    path('addTask/',createTask,name='addTask'),
    path('deleteTask/<int:task_id>',deleteTask,name='delTask'),
    path('markTask/<int:task_id>',markTask,name='markTask'),
    path('allTasks/',renderTasks,name='allTasks'),
    path('',landingPage,name='landingPage'), 
]
handler404=custom_404