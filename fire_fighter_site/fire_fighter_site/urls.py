from django.conf.urls import patterns, include, url
from fire_fighter_site.views.presentation import account, training, certifying, administrator, certifications
from fire_fighter_site.views.ajax import certifying_response, definition_response

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # presentations views
    url(r'^certifications$',       certifications.display),

    url(r'^account/registration$',  account.registration),
    url(r'^account/login$',         account.login),
    url(r'^account/logout$',        account.logout),
    url(r'^account/modification$',  account.modify),
    
    url(r'^training/display$',      training.display),
    
    url(r'^certifying/display$',    certifying.display),
    url(r'^certifying/filter$',     certifying_response.candidate_filter),

    url(r'^administrator/definition$',      administrator.definition),
    url(r'^administrator/definition/pull/requirement$',      definition_response.pull_requirement),
    url(r'^administrator/definition/pull/certification$',    definition_response.pull_certification),
    url(r'^administrator/definition/push/requirement$',      definition_response.push_requirement),
    url(r'^administrator/definition/push/certification$',    definition_response.push_certification),
    
    #catch all redirects to login
    url(r'^.*$',                      account.login),
)