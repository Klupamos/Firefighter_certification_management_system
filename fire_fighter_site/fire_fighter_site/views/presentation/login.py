from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect


from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks

from candidate.models import Candidate, NewCandidateForm

def display(request):

    if (request.user.is_authenticated()):
        return redirect('/account_info')
    
    errors = None
    if (request.method == 'POST'):
        f = NewCandidateForm(request.POST)
        if f.is_valid():
            submited_candidate = f.save()
        else:
            errors = f.errors
    
    user = auth.authenticate(username='', password='')
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return redirect('/account_info')

            
    template_file = 'login_template.djt'
    context_dict = {}
    context_dict['invalid_login'] = errors
    context_dict['path'] = request.path
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict['login_form'] = NewCandidateForm().as_ul()
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)
