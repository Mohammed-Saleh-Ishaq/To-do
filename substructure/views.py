from asyncio import Task, tasks
from audioop import reverse
from contextlib import redirect_stderr
from re import search
from django.shortcuts import render , redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task 

#login/logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django. contrib.auth import login







# Create your views here.
class CustomLoginView(LoginView):
  template_name = 'substructure/login.html'
  fields='_all_'
  redirect_authenticated_user=True

  def get_success_url(self):
    return reverse_lazy('task')

class RegisterPage(FormView):
  template_name = 'substructure/register.html'
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url= reverse_lazy('task')

  def form_valid(self, form):
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super(RegisterPage, self).form_valid(form)    

  def get(self,*args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('tasks')
    return super(RegisterPage,self).get(*args, **kwargs)  



class TaskList(LoginRequiredMixin, ListView):
 model = Task
 #context_object_name = ' tasks 'i don't know y this does not work on first place by manual type
 context_object_name ='tasks'
  #   return HttpResponse('to do list ')

             # specific user data

 def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['tasks']=context['tasks'].filter(user=self.request.user)
     context['count']=context['tasks'].filter(complete=False).count()
     #search 
     search_input= self.request.GET.get('search-area') or ''
     if search_input:
          context['tasks'] = context['tasks'].filter(
             title__startswith = search_input)
      
     context['search_input']= search_input
     return context

#def index(request):ImportError: attempted relative import with no known parent package for this i
#    return render(request,'substructure/task_list.html') have make this func but it does'nt

class TaskDetail(LoginRequiredMixin, DetailView):
  model = Task
  context_object_name = 'task'#we can write any name eg;work,home etc
  template_name = 'substructure/task.html'# / task.html tha bolke nai aara tha sp remove kare tho aara.
# this class will show view click it will show task

class TaskCreate(LoginRequiredMixin, CreateView):
  model= Task
  fields= ['title', 'description', 'complete']
  success_url= reverse_lazy('task')

  def form_valid(self, form):
    form.instance.user=self.request.user
    return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
  model= Task
  fields= ['title', 'description', 'complete']
  success_url= reverse_lazy('task')

class DeleteView(LoginRequiredMixin, DeleteView):
  model= Task
  context_object_name = 'task'
  success_url = reverse_lazy('task')


