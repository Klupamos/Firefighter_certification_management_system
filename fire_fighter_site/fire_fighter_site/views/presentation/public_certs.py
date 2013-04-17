from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import Requirement, Certification

def display(request):
    nav_links = create_navlinks(request.user)
    context_dict = {}
    context_dict['nav_links'] = nav_links
    
    if (request.user.is_authenticated()):
            
        context_dict['full_cert'] = Certification.objects.filter(candidate = request.user).values('name','requirements__name','certifications__name')
#        
        context_dict['part_cert'] = Certification.objects.exclude(candidate = request.user).filter(Q(requirements__candidate = request.user) | Q(certifications__candidate = request.user)).distinct().values('name', 'requirements__name', 'certifications__name')
        
        context_dict['none_cert'] = Certification.objects.exclude(candidate = request.user).exclude(Q(requirements__candidate = request.user) | Q(certifications__candidate = request.user)).distinct().values('name', 'requirements__name', 'certifications__name')
    else:
        context_dict['none_cert'] = Certification.objects.all()

    return render_to_response('public_certs_template.djt', context_dict)
