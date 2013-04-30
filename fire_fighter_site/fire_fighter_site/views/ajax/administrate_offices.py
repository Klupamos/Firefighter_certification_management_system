from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect

from django.contrib import auth
from django.core.context_processors import csrf

from fire_fighter_site.views.helper import create_navlinks
from candidate.forms import AdministrateOfficesForm
from candidate.models import Candidate, Jurisdiction


def user_name(user):
    return user.get_full_name()
    
def print_jurisdiction(j):
    return str(j)

def response(request):

    if (not request.user.is_authenticated()):
        return redirect('/login')

    if (not request.user.Is_Administrator()):
        return redirect('/account_info') 
    
    


    c_obj = None
    c_id = request.POST.get('candidate', '')
    try:
        c_obj = Candidate.objects.get(id=c_id)
    except:
        print ""
    
    j_obj = None
    j_id = request.POST.get('jurisdiction', '')
    try:
        j_obj = Jurisdiction.objects.get(id=c_id)
    except:
        print ""
        
    func_ptr = {
        'CD': {
            'A': lambda:  "("+c_obj.get_full_name()+").is_active = true", #"c_obj.is_active = true",
            'R': lambda:  "("+c_obj.get_full_name()+").is_active = false",#"c_obj.is_active = false",
        },
        'TO': {
            'A': lambda:  str(j_obj)+".training_officer.add("+c_obj.get_full_name()+")",     #j_obj.training_officer.add(c_obj)
            'R': lambda:  str(j_obj)+".training_officer.remove("+c_obj.get_full_name()+")",  #j_obj.training_officer.add(c_obj)
        },
        'CO': {
            'A': lambda:  str(j_obj)+".certifying_officer.add("+c_obj.get_full_name()+")",     #"j_obj.certifying_officer.add(c_obj)"
            'R': lambda:  str(j_obj)+".certifying_officer.remove("+c_obj.get_full_name()+")",     #"j_obj.certifying_officer.add(c_obj)"
        },
        'AD': {
            'A': lambda:  "Administrators.objects.add("+c_obj.get_full_name()+")",
            'R': lambda:  "Administrators.objects.remove("+c_obj.get_full_name()+")",
        },
    }  
    action_id = request.POST.get('action', '')
    office_id = request.POST.get('office', '')
        
    context_dict = {}
    context_dict['user'] = (
        func_ptr.get(office_id).get(action_id)(),
    )
    
    
    return render_to_response('administrate_offices.djt', context_dict)