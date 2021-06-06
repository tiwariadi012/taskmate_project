from django.shortcuts import redirect, render
from django.http import HttpResponse
#import model and fetch all items by using model.objects.all
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
   if request.method == "POST":
      form = TaskForm(request.POST or None)
      if form.is_valid():
         instance = form.save(commit=False)
         instance.manage = request.user
         instance.save()
      messages.success(request,"New task added!")
      return redirect('todolist')
   else:
      #all_tasks = TaskList.objects.all()
      all_tasks = TaskList.objects.filter(manage=request.user)

      paginator = Paginator(all_tasks,3)
      page = request.GET.get('pg')
      all_tasks = paginator.get_page(page)
      #  context = {'welcome_text':"welcome ToDo List.",
      #  }
      return render(request,'todolist.html',{'all_tasks': all_tasks})
         # return HttpResponse("welcome to task page")

def index(request):
    context = {'index_text':"welcome index page.",
    }
    return render(request,'index.html',context)

@login_required
def contact(request):
    context = {'contact_text':"welcome contact page.",
    }
    return render(request,'contact.html',context)
   # return HttpResponse("welcome to task page")

@login_required
def about(request):
    context = {'about_text':"welcome about page.",
    }
    return render(request,'about.html',context)

@login_required
def delete_task(request, task_id):
   task = TaskList.objects.get(pk=task_id)
   if task.manage == request.user:
      task.delete()

   else:
      messages.error(request,("Access denied"))

   return redirect('todolist')

@login_required
def edit_task(request, task_id):

   if request.method == "POST":
      task = TaskList.objects.get(pk=task_id)
      form = TaskForm(request.POST or None, instance = task)
      if form.is_valid():
         instance = form.save(commit=False)
         instance.manage = request.user
         instance.save()
         
      messages.success(request,"Task Updated!")
      return redirect('todolist')
   else:
      task_obj = TaskList.objects.get(pk=task_id)      #  context = {'welcome_text':"welcome ToDo List.",
      #  }
      return render(request,'edit.html',{'task_obj': task_obj})
         # return HttpResponse("welcome to task page")
@login_required
def complete_task(request, task_id):
   task = TaskList.objects.get(pk=task_id)
   if task.manage == request.user:
  
      task.done = True
      task.save()
   else:
      messages.error(request,("Access denied"))

   return redirect('todolist')

@login_required
def pending_task(request, task_id):
   task = TaskList.objects.get(pk=task_id)
   task.done = False
   task.save()

   return redirect('todolist')
