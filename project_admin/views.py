from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import *
from django.contrib import messages
from .models import *
from django.forms import formset_factory
from django.views import View
from django.core.mail import EmailMessage
from smtplib import SMTPException
import time
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        rec = Project.objects.all()

        context = {'project': rec}
        return render(request, 'dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def showview(request):
    if request.user.is_authenticated and request.user.is_superuser:
        rec = Project.objects.all()
        return render(request, 'show.html', {'project':rec})
    else:
        return HttpResponseRedirect(reverse('login'))


def deleteview(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            pid = request.POST['pid']
            Project.objects.get(project_id=pid).delete()
        rec = Project.objects.all()
        return render(request, 'delete.html', {'project':rec})
    else:
        return HttpResponseRedirect(reverse('login'))


def details(request, pid):
    if request.user.is_authenticated and request.user.is_superuser:
        rec = Project.objects.get(project_id=pid)
        prog = rec.work_set.all()
        total = len(prog)
        complete = 0
        try:
            complete = int((len([i for i in prog if i.status])/total)*100)
        except:
            pass
        context={
            'project': rec,
            'prog': prog,
            'total': total,
            'complet': complete,
            'pid':pid
        }

        return render(request, 'details.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def createview(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                request.session['project'] = request.POST
                return HttpResponseRedirect(reverse('addprog'))
        form = ProjectForm()
        return render(request, 'create.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('login'))


class ProgrammerFormView(View):
    Prog_FormSet=formset_factory(ProgramerForm)
    template_name="add_prog.html"

    # Overiding the get method
    def get(self,request,*args,**kwargs):
        context={'form':self.Prog_FormSet(),}
        return render(request,self.template_name,context)

    #Overiding the post method
    def post(self, request, *args, **kwargs):
        prog_formset = self.Prog_FormSet(self.request.POST, self.request.FILES)

        if prog_formset.is_valid():
            ProjectForm(request.session['project']).save()
            pid = request.session['project']['project_id']
            project = Project.objects.get(project_id=pid)
            count = 0
            for form in prog_formset:
                Work.objects.create(
                    project_id= project,
                    programmer_id=form.cleaned_data['programmer_id'],
                    task=form.cleaned_data['task'],
                    file=form.cleaned_data['file'],
                    start_time=int(time.time())
                )
                count+=1

            project.no_of_programmer = count
            project.save()
            del request.session['project']

            messages.success(request, 'Project Created Successfully')
            return HttpResponseRedirect(reverse('dashboard'))

        else:
            context={'form':self.Prog_FormSet(),}
            return render(request,self.template_name,context)


def send_mail(request):
    if request.method == 'POST':
        tomail = request.POST['tomail']
        subject = request.POST['subject']
        message = request.POST['message']

        mail = EmailMessage(subject, message, to=[tomail])

        try:
            if len(request.FILES):
                for file in request.FILES.getlist('file'):
                    mail.attach(file.name, file.read(), file.content_type)

            mail.send()
            messages.success(request, 'Email sent Successfully...')
        except (SMTPException, Exception) as e :
            messages.error(request, 'There was an error sending an email: ' + e)

    return HttpResponseRedirect(reverse('dashboard'))


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    labels=[]
    default_items=[]

    def get(self, request,pid, format=None):
        labels = []
        default_items = []
        rec = Project.objects.get(project_id=pid)
        prog = rec.work_set.filter(status=True)

        for p in prog:
            labels.append(str(p.programmer_id))
            time = round((p.end_time - p.start_time)/3600, 2)
            default_items.append(time)

        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
