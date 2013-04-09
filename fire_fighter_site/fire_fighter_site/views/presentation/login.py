from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect


from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import Candidate
from candidate.forms import CandidateLoginForm


def display(request):

    if (request.user.is_authenticated()):
        return redirect('/account_info')
    
    errors = []
    if (request.method == 'POST'):
        user = auth.authenticate(username=request.POST.get('email_address',''), password=request.POST.get('password',''))

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/account_info')
        else:
            errors.append('Invalid login credentials')
            
    template_file = 'login_template.djt'
    context_dict = {}
    context_dict['invalid_login'] = errors
    context_dict['path'] = request.path
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict['login_form'] = CandidateLoginForm().as_ul()
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)
