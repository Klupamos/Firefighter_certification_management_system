from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect


class anchor(object):
    def __init__(self, href, text):
        self.href = href
        self.text = text

def create_navlinks(request):
    nav_links = []
    # Note these hardcoded if statments need to be changed out for permissions
    if request.user.is_authenticated():
        nav_links.append(anchor("/account_info","Account Information"))
        nav_links.append(anchor("/account_certs", "Account Certificates"))
        if request.user.username == 'train':
            nav_links.append(anchor("/training", "Training Officer"))
        if request.user.username == 'certify':
            nav_links.append(anchor("/certifying", "Certifying Officer"))
        if request.user.username == 'admin':
            nav_links.append(anchor("/admin", "Administration"))
        nav_links.append(anchor("/public_certs", "view certificates"))
        nav_links.append(anchor("/logout", "logout"))
    else:
        nav_links.extend([anchor("/login", "login"), anchor("/create", "create account"), anchor("/public_certs", "view certificates")])
    return nav_links


from django.contrib import auth
from django.contrib.auth import logout
from django.core.context_processors import csrf
def login_view(request):

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
    context_dict['nav_links'] = create_navlinks(request)
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)

def logout_view(request):
    auth.logout(request)
    return redirect('/login')

def create_account_view(request):
    nav_links = create_navlinks(request)
    context_dict = {'nav_links': nav_links}
    return render_to_response('create_account_template.djt', context_dict)

def public_certs_view(request):
    nav_links = create_navlinks(request)
    context_dict = {'nav_links': nav_links}
    return render_to_response('public_certs_template.djt', context_dict)

def account_info_view(request):
    nav_links = create_navlinks(request)
    context_dict = {'nav_links': nav_links}
    return render_to_response('account_info_template.djt', context_dict)

def account_certs_view(request):
    nav_links = create_navlinks(request)
    context_dict = {'nav_links': nav_links}
    return render_to_response('account_certs_template.djt', context_dict)

def training_view(request):
    nav_links = create_navlinks(request)
    context_dict = {'nav_links': nav_links}
    return render_to_response('training_template.djt', context_dict)

def certifying_view(request):
    nav_links = create_navlinks(request)
    context_dict = {'nav_links': nav_links}
    return render_to_response('certifying_template.djt', context_dict)

def admin_view(request):
    nav_links = create_navlinks(request)
    context_dict = {'nav_links': nav_links}
    return render_to_response('admin_template.djt', context_dict)
