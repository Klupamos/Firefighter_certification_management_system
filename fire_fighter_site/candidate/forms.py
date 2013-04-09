## some classes that auto generate HTML forms
## https://docs.djangoproject.com/en/dev/topics/forms/modelforms/
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from candidate.models import * 

class CertificationForm(ModelForm):
    class Meta:
        model = Certification

        
class RequirementForm(ModelForm):
    class Meta:
        model = Requirement


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


        
class UpdateCandidateForm(ModelForm):
    fire_fighter_ID = forms.CharField()
    class Meta:
        model = get_user_model()
        exclude = ('password',)
        widgets = {
            'fire_fighter_ID': forms.TextInput(attrs={'disabled':True, 'name':'', 'value':'XXXX####'}), # candidate.get_firefighter_id()
            }
            
class UpdateUserForm(ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    old_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ('email_address', 'new_password', 'confirm_password', 'old_password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

            
class NewJurisdictionForm(ModelForm):
    class Meta:
        model = Jurisdiction
        exclude = ('training_officer', 'certifying_officer',)

        
class CandidateTransferRequestForm(ModelForm):
    class Meta:
        model = Transfer_Request
        exclude = ('candidate', 'TO_approval')

        
class TrainingTransferApprovalForm(ModelForm):
    class Meta:
        model = Transfer_Request
        widgets = {
            'candidate': forms.TextInput(attrs={'disabled':True}),
            }

            
class AdminTransferApprovalForm(ModelForm):
    Admin_approval = forms.CheckboxInput
    class Meta:
        model = Transfer_Request
        exclude = ('TO_approval',)
        widgets = {
            'candidate': forms.TextInput(attrs={'disabled':True}),
            }

            
class AdminCertificationApprovalForm(ModelForm):
    class Meta:
        model = candidate_earned_certification

        
        
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
        
        

