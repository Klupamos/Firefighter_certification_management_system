from django.conf.urls import patterns, include, url
from fire_fighter_site.views.presentation import login, logout, candidate_registration, public_certs, account_info, training, certifying, admin
from fire_fighter_site.views.ajax import administrate_offices

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # presentations views
    url(r'^$',                      login.display),
    url(r'^login$',                 login.display),
    url(r'^logout$',                logout.display),
    url(r'^candidate_registration$',candidate_registration.display),
    url(r'^public_certs$',          public_certs.display),
    url(r'^account_info$',          account_info.display),
    url(r'^account_certs$',         public_certs.display),
    url(r'^training$',              training.display),
    url(r'^certifying$',            certifying.display),
    url(r'^admin$',                 admin.display),
    url(r'^admin/display/([a-zA-Z]*)$',admin.display),  # Non ajax fallback for view candidate infomation

    # ajax views
    url(r'^admin/offices$', administrate_offices.response),
)
