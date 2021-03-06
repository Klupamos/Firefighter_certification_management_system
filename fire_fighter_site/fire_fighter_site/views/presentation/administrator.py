from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect

from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.forms import  RequirementDefinitionForm, CertificationDefinitionForm
from candidate.models import Candidate

    
def definition(request):
    if (not request.user.is_authenticated()):
        return redirect('/login')

    if (not request.user.Is_Administrator()):
        return redirect('/account_info') 

    context_dict = {}
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict.update(csrf(request))
    context_dict['requirement_form'] = {
        'elements': RequirementDefinitionForm(),
        'push_addr': "/administrator/definition/push/requirement",
        'pull_addr': "/administrator/definition/pull/requirement",
    }
    context_dict['certification_form'] = {
        'elements': CertificationDefinitionForm(),
        'push_addr': "/administrator/definition/push/certification",
        'pull_addr': "/administrator/definition/pull/certification",
    }
    return render_to_response('admin_definition.djt', context_dict)
