from django.conf.urls import url
from . import views as adminview


urlpatterns = [

    url(r'^dashboard/$', adminview.dashboard, name='dashboard'),
    url(r'^dashboard/send_mail$', adminview.send_mail, name='send_mail'),
    url(r'^dashboard/create/$', adminview.createview, name='createview'),
    url(r'^dashboard/create/add_prog$', adminview.ProgrammerFormView.as_view(), name='addprog'),
    url(r'^dashboard/show/$', adminview.showview, name='showview'),
    url(r'^dashboard/show/(?P<pid>[0-9A-Za-z_\-]+)/',adminview.details, name='details'),
    url(r'^dashboard/delete/$', adminview.deleteview, name='deleteview'),
    url(r'^api/chart/(?P<pid>[a-zA-Z0-9_]+)/$', adminview.ChartData.as_view()),
]