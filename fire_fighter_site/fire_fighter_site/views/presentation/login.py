from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect


from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import Candidate
from candidate.forms import UserLoginForm


def display(request):

    if (request.user.is_authenticated()):
        return redirect('/account_info')
    
    errors = []
    user = None
    if (request.method == 'POST'): 
        user_record = UserLoginForm(request.POST)
        errors.append(user_record)
        if user_record.is_valid():
            user = auth.authenticate(username=user_record.user_name, password=user_record.password)
        #else:
            #errors.extend(user_record.errors)
    
    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect('/account_info')

            
    template_file = 'login_template.djt'
    context_dict = {}
    context_dict['invalid_login'] = errors
    context_dict['path'] = request.path
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict['login_form'] = UserLoginForm().as_ul()
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)
