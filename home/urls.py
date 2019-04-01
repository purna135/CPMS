from django.conf.urls import url
from . import views as home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', home_view.indexview, name='indexview'),
    url( r'^login/$',home_view.signinview, name="login"),

    url(r'^register/$', home_view.signupview, name='register'),

    url(r'^logout/$', home_view.logoutview, name='logout'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',home_view.activate, name='activate'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html", email_template_name="password_reset_email.html", subject_template_name="password_reset_subject.txt"), name='password_reset'),

    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),

]