import json
from django.shortcuts import redirect, HttpResponse
from candidate.models import Certification, Jurisdiction
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist

def response(request):
    
    if not request.user.is_authenticated() or not request.user.Is_Authorized('CO'):
        raise PermissionDenied
    
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
    
    result = []
    if j_obj and c_obj:
        result.extend([cand.get_full_name() for cand in j_obj.Eligible_Candidates_List(c_obj)])
        
    return HttpResponse(json.dumps(result), mimetype='application/json')