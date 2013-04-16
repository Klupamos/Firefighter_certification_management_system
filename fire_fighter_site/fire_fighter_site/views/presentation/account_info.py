from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect

from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import Candidate
from candidate.forms import ChangeCandidateForm



def display(request):

   # if (request.user.is_authenticated()):
   #     return redirect('/account_info')

    errors = None
    if (request.method == 'POST'):
        a = Candidate.objects.get(email_address=request.POST.get('email_address'))
        f = ChangeCandidateForm(request.POST,instance=a)
        if a.check_password(request.POST.get('old_password')):
            if request.POST.get('new_password') == request.POST.get('confirm_password') and request.POST.get('new_password') != '':
                a.set_password(request.POST.get('new_password'))
                a.save()


        f.save()
        # if f.is_valid():
        #     print f
        #    # submited_candidate = f.save(commit=False) # get a candidate object without saving to the database
        #    # submited_candidate.set_password(f.cleaned_data['password']) # hash and set the supplied password
        #    # submited_candidate.save()   # Now save to the database
        #    # auth.login(request, submited_candidate)
        #     f.save()
        # else:
        #     errors = f.errors

    template_file = 'account_info_template.djt'
    context_dict = {}
    context_dict['invalid_login'] = errors
    context_dict['path'] = request.path
    context_dict['nav_links'] = create_navlinks(request.user)
    usr_dic = {
        'email_address':request.user.email_address,
#        'password':request.user.password,
#       'confirm_password',
        'first_name': request.user.first_name,
        'middle_initial':request.user.middle_initial,
        'last_name':request.user.last_name,
        'suffix':request.user.suffix,
        'phone_number':request.user.phone_number,
        'street_address':request.user.street_address,
        'city_name':request.user.city_name,
        'postal_code':request.user.postal_code,
        'state_abrv':request.user.street_address,
        'jurisdiction':request.user.jurisdiction,}

    tmp = ChangeCandidateForm(initial=usr_dic)
    tmp.fields['email_address'].widget.attrs['disabled']=True
    context_dict['login_form'] = tmp.as_ul()
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)
