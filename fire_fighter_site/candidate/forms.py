## some classes that auto generate HTML forms
## https://docs.djangoproject.com/en/dev/topics/forms/modelforms/
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model

class CertificationForm(ModelForm):
    class Meta:
        model = Certification

        
class RequirementForm(ModelForm):
    class Meta:
        model = Requirement


class UserLoginForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('user_name', 'password',)
        
        
class NewCandidateForm(ModelForm):
    class Meta:
        model = get_user_model()
        exclude = ('fire_fighter_ID', 'certifications', 'requirements',)

        
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
