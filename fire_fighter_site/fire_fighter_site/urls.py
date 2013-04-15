from django.conf.urls import patterns, include, url
from fire_fighter_site.views.presentation import login, logout, candidate_registration, public_certs, account_info, training, certifying_view, admin
from fire_fighter_site.views.ajax import administrate_offices, certifying_view_response

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # presentations views
    url(r'^$',                      login.display),
    url(r'^login$',                 login.display),
    url(r'^logout$',                logout.display),
    url(r'^candidate_registration$',candidate_registration.display),
    url(r'^certification_list$',    public_certs.display),
    url(r'^account_info$',          account_info.display),
    url(r'^training$',              training.display),
    url(r'^certifying$',            certifying_view.display),
    url(r'^admin$',                 admin.display),
    url(r'^admin/display/([a-zA-Z]*)$',admin.display),  # Non ajax fallback for view candidate infomation

    # ajax views
    url(r'^admin/offices$', administrate_offices.response),
    url(r'^certify/pre_screen$', certifying_view_response.response),
)
