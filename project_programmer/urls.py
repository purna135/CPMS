from django.conf.urls import url
from . import views as prog_view

urlpatterns = [
    url(r'^myaccount/$', prog_view.prog_dashboard, name='prog_dash'),

    url(r'^myaccount/current_project/$', prog_view.current_project, name='current_project'),

    url(r'^myaccount/current_project/(?P<pid>[0-9A-Za-z_\-]+)/$', prog_view.show, name='current_show'),

    url(r'^myaccount/upload/$', prog_view.upload, name='upload_project'),

    url(r'^myaccount/old_project/$', prog_view.old_project, name='old_project'),

    url(r'^myaccount/old_project/(?P<pid>[0-9A-Za-z_\-]+)/$', prog_view.show, name='old_show'),

    url(r'^myaccount/download/(?P<pid>[0-9A-Za-z_\-]+)/$', prog_view.download, name='download'),

    url(r'^myaccount/send_mail/$', prog_view.send_mail, name='send_mail'),

    url(r'^api/chart/data/(?P<user>[a-zA-Z0-9_]+)/$', prog_view.ChartData.as_view()),

    ]