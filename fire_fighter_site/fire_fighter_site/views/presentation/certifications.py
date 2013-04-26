from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import Requirement, Certification, candidate_earned_requirement, candidate_earned_certification

from django.db.models import Q, F
from operator import __or__, __and__

def display(request):
    nav_links = create_navlinks(request.user)
    context_dict = {}
    context_dict['nav_links'] = nav_links
    
    debug = []
    if (request.user.is_authenticated()):
        
        full_arr = []
        for cert in Certification.objects.filter(candidate = request.user).distinct().prefetch_related('child_requirements', 'child_certifications'):
            full_arr.append({
                'name': cert.name,
                'description':cert.description,
                'expiration':candidate_earned_certification.objects.filter(certification = cert, candidate = request.user).values('expiration_date')[0]['expiration_date'],
                'sub_reqs': cert.child_requirements.values('name'),
                'sub_certs': cert.child_certifications.values('name'),
            })
        debug = full_arr
        
        part_arr = []
        for cert in Certification.objects.exclude(candidate = request.user).filter(Q(child_requirements__candidate = request.user) | Q(child_certifications__candidate = request.user)).distinct().prefetch_related('child_requirements', 'child_certifications'):
            all_child_req_list = []
            earned_child_req_list = [{'name':req['name'], 'earned':True} for req in Requirement.objects.filter(candidate = request.user).filter(parent_certification = cert).values('name')]
            unearned_child_req_list = Requirement.objects.exclude(candidate = request.user).filter(parent_certification = cert).values('name')
            all_child_req_list.extend(earned_child_req_list)
            all_child_req_list.extend(unearned_child_req_list)
            
            
            all_child_cert_list = []
            earned_child_cert_list = [{'name':c['name'], 'earned':True} for c in Certification.objects.filter(candidate = request.user).filter(parent_certification = cert).values('name')]
            unearned_child_cert_list = Certification.objects.exclude(candidate = request.user).filter(parent_certification = cert).values('name')
            all_child_cert_list.extend(earned_child_cert_list)
            all_child_cert_list.extend(unearned_child_cert_list)
            
            part_arr.append({
                'name': cert.name,
                'description':cert.description,

                'sub_reqs': all_child_req_list,
                'sub_certs': all_child_cert_list,
            })
        
        none_arr = []
        for cert in Certification.objects.exclude(candidate = request.user).exclude(child_requirements__candidate = request.user).exclude(child_certifications__candidate = request.user).distinct().prefetch_related('child_requirements', 'child_certifications'):
            none_arr.append({
                'name': cert.name,
                'description':cert.description,
                'sub_reqs': cert.child_requirements.values('name'),
                'sub_certs': cert.child_certifications.values('name'),
            })
            
#        debug = none_arr
            
        
        context_dict['full_cert'] = full_arr
        context_dict['part_cert'] = part_arr
        context_dict['none_cert'] = none_arr
    else:
        none_arr = []
        for cert in Certification.objects.all().distinct().prefetch_related('child_requirements', 'child_certifications'):
            none_arr.append({
                'name': cert.name,
                'description':cert.description,
                'sub_reqs': cert.child_requirements.values('name'),
                'sub_certs': cert.child_certifications.values('name'),
            })
        context_dict['none_cert'] = none_arr   
            
        
    context_dict['x'] = debug
    return render_to_response('public_certs_template.djt', context_dict)
