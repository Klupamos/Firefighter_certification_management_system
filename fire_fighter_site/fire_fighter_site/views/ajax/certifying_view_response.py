from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect, HttpResponse

from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.forms import PreScreenForm
from candidate.models import Certification, Jurisdiction

from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson

def response(request):

    if (not request.user.is_authenticated()):
        return redirect('/login')

    if (not request.user.Is_Certifying_Officer()):
        return redirect('/account_info') 
        
    
    
    c_obj = None
    c_id = request.POST.get('certification', 0)
    try:
        c_obj = Certification.objects.get(id=c_id)
    except ObjectDoesNotExist:
        pass
    
    j_obj = None
    j_id = request.POST.get('jurisdiction', 0)
    try:
        j_obj = Jurisdiction.objects.get(id=j_id)
    except ObjectDoesNotExist:
        pass
    
    
    
    context_dict = {}    
    if j_obj and c_obj:
        result = [cand.get_full_name() for cand in j_obj.Eligible_Candidates_List(c_obj)]
        context_dict['cand_list'] = "|".join(result)
    
    return render_to_response('certifying_view_response_template.djt', context_dict)