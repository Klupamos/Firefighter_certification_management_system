from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response

from fire_fighter_site.views.helper import create_navlinks
from candidate.models import Requirement, Certification

from django.db.models import Q, F
from operator import __or__, __and__

def display(request):
    nav_links = create_navlinks(request.user)
    context_dict = {}
    context_dict['nav_links'] = nav_links
    
    if (request.user.is_authenticated()):
        full_dict = {}        
        for row in Certification.objects.filter(candidate = request.user).values(
            'name',
            'description',
            'candidate_earned_certification__expiration_date',
            'requirements__name',
            'certifications__name',
        ):
            full_dict.setdefault(row['name'], {})
            full_dict[row['name']]['description'] = row['description']
            full_dict[row['name']]['expiration'] = row['candidate_earned_certification__expiration_date']
            full_dict[row['name']].setdefault('sub_reqs', [])
            if row['requirements__name']:
                full_dict[row['name']]['sub_reqs'].append(row['requirements__name'])
                
            full_dict[row['name']].setdefault('sub_certs', [])
            if row['certifications__name']:
                full_dict[row['name']]['sub_certs'].append(row['certifications__name'])
        
        full_arr = []
        for key in full_dict.keys():
            full_arr.append({'name': key, 'description': full_dict[key]['description'], 'expiration':full_dict[key]['expiration'], 'sub_reqs':full_dict[key]['sub_reqs'], 'sub_certs':full_dict[key]['sub_certs']})
        
        part_dict = {}
        for row in Certification.objects.exclude(candidate = request.user).filter(Q(requirements__candidate = request.user) | Q(certifications__candidate = request.user)).values(
            'name',
            'description',
            'requirements__name',
            'requirements__candidate_earned_requirement',
            'certifications__name',
            'certifications__candidate_earned_certification',
        ):
            print row['requirements__candidate_earned_requirement']
            part_dict.setdefault(row['name'], {})
            part_dict[row['name']]['description'] = row['description']
            part_dict[row['name']].setdefault('sub_reqs', [])            
            if row['requirements__name']:
                part_dict[row['name']]['sub_reqs'].append({
                    'name': row['requirements__name'],
                    'earned': True if row['requirements__candidate_earned_requirement'] != None else False
                })
                
            part_dict[row['name']].setdefault('sub_certs', [])
            if row['certifications__name']:
                part_dict[row['name']]['sub_certs'].append({
                    'name': row['certifications__name'],
                    'earned': True if row['certifications__candidate_earned_certification'] != None else False
                })
        
        part_arr = []
        for key in part_dict.keys():
            part_arr.append({'name': key, 'description': row['description'],  'sub_reqs':part_dict[key]['sub_reqs'], 'sub_certs':part_dict[key]['sub_certs']})
        
        
        context_dict['full_cert'] = full_arr
        context_dict['part_cert'] = part_arr
        context_dict['none_cert'] = Certification.objects.exclude(candidate = request.user).exclude(requirements__candidate = request.user).exclude(certifications__candidate = request.user).prefetch_related('requirements').prefetch_related('certifications')
    else:
        context_dict['none_cert'] = Certification.objects.all().prefetch_related('requirements').prefetch_related('certifications')

    return render_to_response('public_certs_template.djt', context_dict)
