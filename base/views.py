from django.shortcuts import render, redirect
from .models import Project, Skill, Message
from .forms import ProjectForm, MsessageForm
from django.contrib import messages
# Create your views here.


def homepage(request):
    projects = Project.objects.all()

    detailedskills = Skill.objects.exclude(body ='')
    
    skills = Skill.objects.filter(body='')

    form = MsessageForm() 
    
    if request.method == 'POST' :
        form = MsessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your message was successfully sent.')

    context = {'projects' : projects, 'skills' : skills,
            'detailedskills' : detailedskills,'form' : form}
    
    return render(request,'base/home.html', context)




def projectpage(request,pk):
    project= Project.objects.get(id=pk)
    context = {'project': project}
    return render(request, 'base/project.html',context)


def addproject(request):
    form = ProjectForm()

    if request.method == 'POST' :
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form': form}
    return render(request, 'base/project_form.html',context)



def editproject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST' :
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form': form}
    return render(request, 'base/project_form.html',context)



def inboxpage(request):
    inbox = Message.objects.all().order_by('is_read')

    unreadcount = Message.objects.filter(is_read=False).count()
    context = {'inbox': inbox,'unreadcount': unreadcount}
    return render(request,'base/inbox.html',context)


def messagepage(request, pk):
    message = Message.objects.get(id=pk)
    message.is_read = True
    message.save()
    context = {'message': message}
    return render(request,'base/message.html',context)  