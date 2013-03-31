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
        fields = ('user_name', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class NewCandidateForm(ModelForm):
    required_css_class='required'
    class Meta:
        model = get_user_model()
        fields = (
            'user_name',
            'password',
            'first_name',
            'middle_initial',
            'last_name',
            'suffix',
            'phone_number',
            'email_address',
            'street_address',
            'city_name',
            'postal_code',
            'state_abrv',
            'jurisdiction',
        )


        
class UpdateCandidateForm(ModelForm):
    class Meta:
        model = get_user_model()
        widgets = {
            'fire_fighter_ID': forms.TextInput(attrs={'disabled':True, 'name':''}),
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
