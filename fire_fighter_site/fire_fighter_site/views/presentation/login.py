from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect


from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import User, UserLoginForm


def display(request):

    if (request.user.is_authenticated()):
        return redirect('/account_info')
    
    errors = None
    user = None
    if (request.method == 'POST'): 
        u = UserLoginForm(request.POST)
        if u.is_valid():
            user_record = u.save(commit=False)#create a user record but don't save it to the database
            user = auth.authenticate(username=user_record.username, password=user_record.password)
        else:
            errors = u.errors
    
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
