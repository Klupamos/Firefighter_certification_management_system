from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect


from django.core.context_processors import csrf
from fire_fighter_site.views.helper import create_navlinks
from candidate.forms import PreScreenForm

def display(request):

    if not request.user.is_authenticated():
        return redirect('/login')
    
    
    context_dict = {}
    context_dict['nav_links'] = create_navlinks(request.user)
    context_dict['ps_form'] = PreScreenForm(Officer=request.user).as_ul()
    context_dict['form_handel'] = "/certify/pre_screen"
    context_dict.update(csrf(request))

    return render_to_response('certifying_view_template.djt', context_dict)