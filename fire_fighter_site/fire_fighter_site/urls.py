from django.conf.urls import patterns, include, url
from fire_fighter_site.views.presentation import login, logout, candidate_registration, public_certs, account_info, account_certs, training, certifying, admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                      login.display),
    url(r'^login$',                 login.display),
    url(r'^logout$',                logout.display),
    url(r'^candidate_registration$',candidate_registration.display),
    url(r'^public_certs$',          public_certs.display),
    url(r'^account_info$',          account_info.display),
    url(r'^account_certs$',         account_certs.display),
    url(r'^training$',              training.display),
    url(r'^certifying$',            certifying.display),
    url(r'^admin$',                 admin.display),
    url(r'^admin/display/([a-zA-Z]*)$',admin.display),
                       
    # Examples:
    # url(r'^$', 'fire_fighter_site.views.home', name='home'),
    # url(r'^fire_fighter_site/', include('fire_fighter_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
