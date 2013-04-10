from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import Requirement, Certification

def display(request):
    nav_links = create_navlinks(request.user)
    context_dict = {}
    context_dict['nav_links'] = nav_links
    context_dict['all'] = Certification.objects.all()
    return render_to_response('public_certs_template.djt', context_dict)
