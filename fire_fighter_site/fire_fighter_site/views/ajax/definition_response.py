import json
from django.shortcuts import redirect, HttpResponse
from candidate.models import Certification, Requirement
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist

def pull_requirement(request):
    if not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied
    
    if request.method != "POST" or not HttpRequest.is_ajax():
        print "AJAX"
    
    r_obj = None
    r_id = request.POST.get('selection', 0)
    
    if r_id == 0:
        return HttpResponse(json.dumps(None), mimetype='application/json')

    try:
        r_obj = Requirement.objects.filter(id=r_id).values('name')
    except ObjectDoesNotExist:
        pass
    
    return HttpResponse(json.dumps(r_obj), mimetype='application/json')

    
def pull_certification(request):
    if request.method != "POST" or not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied
   
    
    c_obj = None
    c_id = request.POST.get('selection', 0)
    try:
        c_obj = Certification.objects.filter(id=c_id).values('name', 'description', 'requirements', 'certifications', 'months_valid', 'deprecated')
    except ObjectDoesNotExist:
        pass
    
    
    return HttpResponse(json.dumps(c_obj), mimetype='application/json')
    
def push_certification(request):
    if request.method != "POST" or not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied
   
    
    c_obj = None
    c_id = request.POST.get('selection', '0')
    c_name = request.POST.get('name', 'certification_'+c_id)
    c_desc = request.POST.get('description','')
    c_sub_certs = request.POST.getlist('certifications')
    c_sub_reqs = request.POST.getlist('requirements')
    c_deprecated = request.POST.get('deprecated','off')
    c_months_valid = request.POST.get('months_valid',0)
    
    print c_name
    print c_desc
    print c_deprecated
    print c_months_valid
    print c_sub_certs
    print c_sub_reqs

    if c_id == '0':
        c_obj = Certification() # new unsaved certification

    try:
        c_obj = Certification.objects.get(id=c_id)
    except ObjectDoesNotExist:
        pass
    
    response = False
    if c_obj:
        c_obj.name = c_name
        c_obj.description = c_desc
        c_obj.months_valid = c_months_valid
        c_obj.deprecated = c_deprecated

        c_obj.Add_Certifications(Certification.objects.filter(id__in = sub_certs))
        c_obj.Add_Requirements(Requirement.objects.filter(id__in = c_sub_reqs))
        c_obj.save()
        response = True
        
    return HttpResponse(json.dumps(response), mimetype='application/json')
    
def push_requirement(request):
    if request.method != "POST" or not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied
        
    r_obj = None
    r_id = request.POST.get('selection', '0')
    r_name = request.POST.get('name', 'requirement_'+r_id)
    
    if r_id == '0':
        r_obj = Requirement() # new unsaved Requirement

    try:
        r_obj = Requirement.objects.get(id=r_id)
    except ObjectDoesNotExist:
        pass
    
    response = False
    if r_obj:
        r_obj.name = r_name
        r_obj.save()
        response = True
        
    
    
    return HttpResponse(json.dumps(response), mimetype='application/json')