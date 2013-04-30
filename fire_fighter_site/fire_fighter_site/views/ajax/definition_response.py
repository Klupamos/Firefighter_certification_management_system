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
        result = [True, {'name':r_obj.name}]
    except ObjectDoesNotExist:
        result = [False, "Invalid Input"]
    except ValueError:
        result = [False, "Invalid Input"]

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
        result = [True, {
            'name':c_obj.name,
            'description': c_obj.description,
            'child_requirements': [x['id'] for x in c_obj.child_requirements.values('id')],
            'child_certifications': [x['id'] for x in c_obj.child_certifications.values('id')],
            'months_valid': c_obj.months_valid,
            'deprecated': c_obj.deprecated,
        }]
    except ObjectDoesNotExist:
        result = [False, "Invalid Input"]
    except ValueError:
        result = [False, "Invalid Input"]


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
    c_sub_certs = request.POST.getlist('child_certifications')
    print c_sub_certs
    c_sub_reqs = request.POST.getlist('child_requirements')
    print c_sub_reqs
    c_deprecated = request.POST.get('deprecated','off')
    c_months_valid = request.POST.get('months_valid',0)

    if c_id == '0':
        c_obj = Certification() # new unsaved certification
        c_obj.save()

    try:
        c_obj = Certification.objects.get(id=c_id)
    except ObjectDoesNotExist:
        pass

    print c_obj
    response = [False, "Default response"]
    if c_obj:
        try:
            c_obj.child_certifications = []
            c_obj.Add_Certifications(*Certification.objects.filter(id__in = c_sub_certs))
        except:
            response = [False, "Cyclic dependency detected"]
        else:
            c_obj.child_requirements = []
            c_obj.Add_Requirements(*Requirement.objects.filter(id__in = c_sub_reqs))
            c_obj.name = c_name
            c_obj.description = c_desc
            c_obj.months_valid = c_months_valid
            c_obj.deprecated = c_deprecated
            c_obj.save()
            response = [True, "Certification updated", c_obj.id]
        
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
    
    response = [False, "Default response"]
    if r_obj:
        r_obj.name = r_name
        r_obj.save()
        response = [True, "Requirement Updated", r_obj.id]
        
    
    
    return HttpResponse(json.dumps(response), mimetype='application/json')