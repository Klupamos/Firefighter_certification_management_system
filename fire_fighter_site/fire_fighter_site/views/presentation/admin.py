from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect

from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.forms import AdministrateOfficesForm
from candidate.models import Candidate

def display(request):

    if (not request.user.is_authenticated()):
        return redirect('/login')

    if (not request.user.is_administrator()):
        return redirect('/account_info') 
    
    
    context_dict = {}
    context_dict['form'] = AdministrateOfficesForm()
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict.update(csrf(request))
    return render_to_response('admin_template.djt', context_dict)