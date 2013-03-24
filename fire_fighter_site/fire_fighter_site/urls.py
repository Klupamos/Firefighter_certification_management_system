from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'fire_fighter_site.views.login_view'),
    url(r'^login$', 'fire_fighter_site.views.login_view'),
    url(r'^logout$', 'fire_fighter_site.views.logout_view'),
    url(r'^create$', 'fire_fighter_site.views.create_account_view'),
    url(r'^public_certs$', 'fire_fighter_site.views.public_certs_view'),
    url(r'^account_info$', 'fire_fighter_site.views.account_info_view'),
    url(r'^account_certs$', 'fire_fighter_site.views.account_certs_view'),
    url(r'^training$', 'fire_fighter_site.views.training_view'),
    url(r'^certifying$', 'fire_fighter_site.views.certifying_view'),
    url(r'^admin$', 'fire_fighter_site.views.admin_view'),

                       
    # Examples:
    # url(r'^$', 'fire_fighter_site.views.home', name='home'),
    # url(r'^fire_fighter_site/', include('fire_fighter_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
