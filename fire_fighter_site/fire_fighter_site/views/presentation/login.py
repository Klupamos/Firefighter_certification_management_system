from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect


from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks

def display(request):

    if (request.user.is_authenticated()):
        return redirect('/account_info')

    sent_username = request.POST.get('username', 'default')
    sent_password = request.POST.get('password', 'default')

    user = auth.authenticate(username=sent_username, password=sent_password)
    context_dict = {}
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return redirect('/account_info')
    else:
        if user is None and sent_username is not 'default':
            context_dict['invalid_login'] = "Invalid login"

    template_file = 'login_template.djt'
    context_dict['path'] = request.path
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)
