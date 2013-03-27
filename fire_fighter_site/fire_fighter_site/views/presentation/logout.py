from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect

from django.contrib.auth import logout

def display(request):
    logout(request)
    return redirect('/login')
