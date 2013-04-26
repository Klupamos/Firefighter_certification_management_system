from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.template import Context, Template
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist

from fire_fighter_site.views.helper import create_navlinks

from candidate.models import Candidate
from candidate.forms import NewCandidateForm, CandidateLoginForm, ChangeCandidateForm

def registration(request):
    if (request.user.is_authenticated()):
        return redirect('/account/login')
    
    errors = None
    form = NewCandidateForm(request.POST or None)
    if (request.method == 'POST'):
        if form.is_valid():
            submited_candidate = form.save(commit=False) # get a candidate object without saving to the database
            submited_candidate.set_password(form.cleaned_data['confirm_password']) # hash and set the supplied password
            
            # make a request rather than manually set the jurisdiction
            submited_candidate.Request_Jurisdiction_Transfer(form.cleaned_data['jurisdiction'])
            submited_candidate.jurisdiction = None
            
            submited_candidate.save()   # Now save to the database
            new_user = auth.authenticate(
                username = form.cleaned_data['email_address'],
                password = form.cleaned_data['confirm_password'],
            )
            auth.login(request, new_user)
            return redirect('/account/modification')
        else:
            errors = form.errors
            
    template_file = 'candidate_registration_template.djt'
    context_dict = {}
    context_dict['invalid_login'] = errors
    context_dict['path'] = request.path
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict['login_form'] = form.as_ul()
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)

def login(request):
    if (request.user.is_authenticated()):
        return redirect('/account/modification')
    
    errors = []
    if (request.method == 'POST'):
        user = auth.authenticate(username=request.POST.get('email_address',''), password=request.POST.get('password',''))

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/account/modification')
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

def logout(request):
    auth.logout(request)
    return redirect('/account/login')

    
from django.forms.models import modelform_factory
def modify(request):
    if not request.user.is_authenticated():
        return redirect('/account/login')
        

    
    errors = None
    cand = request.user
    form = ChangeCandidateForm(request.POST or None, instance = cand)
    if (request.method == 'POST'):
        if form.is_valid() and cand.check_password(form.cleaned_data['old_password']):
            print "PASSED"
            if form.cleaned_data['new_password'] and form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                # update password
                print "Changing password to: '" + form.cleaned_data['new_password'] +"'"
                cand.set_password(form.cleaned_data['new_password'])
            
            orig = Candidate.objects.get(pk = cand.pk)
            if orig.jurisdiction ==  form.cleaned_data['jurisdiction']:
                cand.Revoke_Transfer_Request()
            else:
                cand.Request_Jurisdiction_Transfer(form.cleaned_data['jurisdiction'])
                errors = "Transfer Request Submitted"                
                

    template_file = 'account_info_template.djt'
    context_dict = {}
    context_dict['invalid_login'] = errors
    context_dict['path'] = request.path
    context_dict['nav_links'] = create_navlinks(cand)
    if False:
        form = ChangeCandidateForm(initial = {
            'email_address':    cand.email_address,
            'first_name':       cand.first_name,
            'middle_initial':   cand.middle_initial,
            'last_name':        cand.last_name,
            'suffix':           cand.suffix,
            'phone_number':     cand.phone_number,
            'street_address':   cand.street_address,
            'city_name':        cand.city_name,
            'postal_code':      cand.postal_code,
            'state_abrv':       cand.street_address,
            'jurisdiction':     cand.jurisdiction,
        })
    
    context_dict['login_form'] = form.as_ul()
    
    context_dict.update(csrf(request))
    return render_to_response(template_file, context_dict)
