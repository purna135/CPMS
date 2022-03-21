from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from project_admin.models import *
from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.contrib import messages
import time
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


def prog_dashboard(request):
    if request.user.is_authenticated:
        current_pro = Project.objects.filter(work__programmer_id=request.user, work__status=False)
        complete_pro = Project.objects.filter(work__programmer_id=request.user, work__status=True)

        request.session["current_pro"] = len(current_pro)
        request.session["complete_pro"] = len(complete_pro)

        context ={}

        return render(request, 'prog_dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def current_project(request):
    if request.user.is_authenticated:
        rec = Project.objects.filter(work__programmer_id=request.user, work__status=False)
        context = {'project': rec}
        return render(request, 'current_project.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def old_project(request):
    if request.user.is_authenticated:
        rec = Project.objects.filter(work__programmer_id=request.user, work__status=True)
        context = {'project':rec}
        return render(request, 'old_prog.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def show(request, pid):
    if request.user.is_authenticated:
        work = Work.objects.get(project_id__project_id=pid, programmer_id__username=request.user)
        project = Project.objects.get(project_id=pid)
        context = {
            'work': work,
            'project':project,
        }

        return render(request, 'prog_show.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        pid = request.POST['pid']
        file = request.FILES['file']

        project = Project.objects.get(project_id=pid)
        work = Work.objects.get(project_id__project_id=pid, programmer_id__username=request.user)
        work.file = file
        work.status = True
        work.end_time=int(time.time())
        project.complete_part = project.complete_part + 1
        project.save()
        work.save()

    rec = Project.objects.filter(work__programmer_id=request.user, work__status=False)
    context = {'project':rec}
    return render(request, 'project_upload.html', context)


def download(request, pid):
    work = Work.objects.get(project_id__project_id=pid, programmer_id__username=request.user)

    filename = work.file.name.split('/')[-1]
    response = HttpResponse(work.file, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response


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
    return HttpResponseRedirect(reverse('prog_dash'))


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    labels=[]
    default_items=[]

    def get(self, request,user, format=None):
        labels = []
        default_items = []
        work = Work.objects.filter(programmer_id__username=user, status=True)
        for w in work:
            time = round((w.end_time - w.start_time)/3600, 2)
            labels.append(str(w.project_id))
            default_items.append(time)

        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
