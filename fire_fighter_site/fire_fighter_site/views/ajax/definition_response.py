import json
from django.shortcuts import redirect, HttpResponse
from candidate.models import Certification, Requirement
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from candidate.forms import  RequirementDefinitionForm, CertificationDefinitionForm

def pull_requirement(request):
    if not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied
    
    if request.method != "POST" or not request.is_ajax():
        raise PermissionDenied

    result = None
    r_id = request.REQUEST.get('object_id', 0)

    if r_id == 0:
        return HttpResponse(json.dumps(None), mimetype='application/json')

    try:
        r_obj = Requirement.objects.get(id=r_id)
        result = ({'name':r_obj.name}, True)
    except ObjectDoesNotExist:
        result = ("Invalid Input", False)
    except ValueError:
        result = ("Invalid Input", False)

    return HttpResponse(json.dumps(result), mimetype='application/json')

    
def pull_certification(request):
    if not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied

    if request.method != "POST" or not request.is_ajax():
        raise PermissionDenied


    result = None
    c_id = request.REQUEST.get('object_id', 0)


    try:
        c_obj = Certification.objects.get(id=c_id)
        result = ({
            'name':c_obj.name,
            'description': c_obj.description,
            'child_requirements': [x['id'] for x in c_obj.child_requirements.values('id')],
            'child_certifications': [x['id'] for x in c_obj.child_certifications.values('id')],
            'months_valid': c_obj.months_valid,
            'deprecated': c_obj.deprecated,
        },True)
    except ObjectDoesNotExist:
        result = ("Invalid Input", False)
    except ValueError:
        result = ("Invalid Input", False)


    return HttpResponse(json.dumps(result), mimetype='application/json')
    
def push_certification(request):
    if not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied

    if request.method != "POST" or not request.is_ajax():
        raise PermissionDenied
   
    
    c_obj = None
    c_id = request.POST.get('selection', '0')
    c_name = request.POST.get('name', 'certification_'+c_id)
    c_desc = request.POST.get('description','')
    c_sub_certs = request.POST.getlist('certifications')
    c_sub_reqs = request.POST.getlist('requirements')
    c_deprecated = request.POST.get('deprecated','off')
    c_months_valid = request.POST.get('months_valid',0)

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
        c_obj.save()
        c_obj.Add_Certifications(*Certification.objects.filter(id__in = c_sub_certs))
        c_obj.Add_Requirements(*Requirement.objects.filter(id__in = c_sub_reqs))
        c_obj.save()
        response = True
        
    return HttpResponse(json.dumps(response), mimetype='application/json')
    
def push_requirement(request):
    if not request.user.is_authenticated() or not request.user.Is_Authorized('AD'):
        raise PermissionDenied

    if request.method != "POST" or not request.is_ajax():
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