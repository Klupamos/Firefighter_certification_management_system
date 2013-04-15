## some classes that auto generate HTML forms
## https://docs.djangoproject.com/en/dev/topics/forms/modelforms/
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from candidate.models import * 

class CandidateLoginForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email_address', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class NewCandidateForm(ModelForm):
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    required_css_class='required'
    class Meta:
        model = get_user_model()
        fields = (
            'email_address',
            'password',
            'confirm_password',
            'first_name',
            'middle_initial',
            'last_name',
            'suffix',
            'phone_number',
            'street_address',
            'city_name',
            'postal_code',
            'state_abrv',
            'jurisdiction',
        )
        widgets = {
            'password': forms.PasswordInput(),
        }
       

class PreScreenForm(forms.Form):
        jurisdiction = forms.ChoiceField()
        certification = forms.ChoiceField()
        
        def __init__(self, *args, **kwargs):
            officer = [kwargs.get('Officer', None)]
            del kwargs['Officer']
            super(PreScreenForm, self).__init__(*args, **kwargs)
            
            valid_certifications = [(c['id'], c['name']) for c in Certification.objects.all().order_by('name').values('id', 'name')]
            valid_jurisdictions = []
            if officer:            
                valid_jurisdictions.extend([(j['id'], j['name']) for j in Jurisdiction.objects.filter(certifying_officer__in = officer).values('id', 'name')])
            else:
                valid_jurisdictions.extend([(j['id'], j['name']) for j in Jurisdiction.objects.all().values('id', 'name')])
                
            self.fields['jurisdiction'] = forms.ChoiceField(choices=valid_jurisdictions)
            self.fields['certification'] = forms.ChoiceField(choices=valid_certifications)

class AdministrateOfficesForm(forms.Form):
    candidate =     forms.ChoiceField()
    FORM_ACTIONS = (
        ('A','Activate'),
        ('R','Retire'),
    )
    action =        forms.ChoiceField(choices=FORM_ACTIONS)
    ADDITIONAL_PREMISSIONS = (
        ('CD','Candidate'),
        ('TO','Training Officer'),
        ('CO', 'Certifying Officer'),
        ('AD','Administrator')
    )
    office =      forms.MultipleChoiceField(choices=ADDITIONAL_PREMISSIONS)
    jurisdiction =  forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        super(AdministrateOfficesForm, self).__init__(*args, **kwargs)
        self.fields['candidate'] = forms.ChoiceField(choices=[ 
            (c.id, str(c.get_full_name())) for c in Candidate.objects.all()
        ])

        self.fields['jurisdiction'] = forms.ChoiceField(choices=[ 
            (j.id, str(j.name)) for j in Jurisdiction.objects.all()
        ])
        
        

