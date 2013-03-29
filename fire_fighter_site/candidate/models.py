from django.db import models

##### TO DO #####
#1. Change ER diagram to allow forign key refence between Jurisdiction and User in terms of TA/CO
#2. Need to intigrate User and Candidate into contrib.auth app
#3. Need to finish form generating classes


class Certification(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000)
    requirements = models.ManyToManyField('Requirement', related_name='certifications')
    months_valid = models.IntegerField(default=0) #number of months this certification is valid. 0 for never

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
    
class Requirement(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

# will be used for authentication
class User(models.Model):
    candidate = models.ForeignKey('Candidate', related_name='auth')
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    STATUS_TYPES = (('P','Pending'),('A','Active'),('R','Retired'),)
    status   = models.CharField(max_length=1, choices=STATUS_TYPES, default='P')
    is_admin = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        order_with_respect_to = 'candidate'

class Candidate(models.Model):
    fire_fighter_ID = models.CharField(max_length=10, unique=True) 
    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=1, blank=True)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=4, blank=True)
    phone_number = models.IntegerField(max_length=14, blank=True) # (###)-###-#### ext: ####
    email = models.EmailField(blank=True)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    
    jurisdiction = models.ForeignKey('Jurisdiction', related_name='candidate_list')

    # figure out a way to include a date in these tables
    certifications = models.ManyToManyField(Certification, through='candidate_earned_certification')
    requirements = models.ManyToManyField(Requirement, through='candidate_earned_requirement')

    def __unicode__(self):
        return " ".join(filter(None, (self.first_name, self.middle_initial, self.last_name, self.suffix)))
    
    class Meta:
        ordering = ["last_name", "first_name"]
        unique_together = ('first_name','middle_initial','last_name','suffix')

class candidate_earned_certification(models.Model):
    candidate = models.ForeignKey(Candidate, primary_key=True)
    certifications = models.ForeignKey(Certification)
    date = models.DateField()

class candidate_earned_requirement(models.Model):
    candidate = models.ForeignKey(Candidate, primary_key=True)
    requirements = models.ForeignKey(Requirement)
    date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True)
    # don't know how many of these are necessary
    IFSAC_date = models.DateField()
    IFSAC_number = models.IntegerField()
    PRO_date = models.DateField()
    PRO_number = models.IntegerField()
    company = models.CharField(max_length=20)
    
    
    
class Jurisdiction(models.Model):
    name = models.CharField(max_length=50, unique=True)
    training_officer = models.ManyToManyField(Candidate, related_name='trains_jurisdiction')
    certifying_officer = models.ManyToManyField(Candidate, related_name='certifies_jurisdiction')

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering  = ["name"]    
    
class Transfer_Request(models.Model):
    candidate    = models.ForeignKey(Candidate, related_name='transfer_request', unique=True)
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='requested_transfers', primary_key=True)
    TO_approval  = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        order_with_respect_to = 'candidate'


## some classes that auto generate HTML forms
## https://docs.djangoproject.com/en/dev/topics/forms/modelforms/
from django.forms import ModelForm
from django import forms

class CertificationForm(ModelForm):
    class Meta:
        model = Certification

class RequirementForm(ModelForm):
    class Meta:
        model = Requirement


class UserForm(ModelForm):
    class Meta:
        model = User

class NewCandidateForm(ModelForm):
    class Meta:
        model = Candidate
        exclude = ('fire_fighter_ID', 'certifications', 'requirements',)

class UpdateCandidateForm(ModelForm):
    class Meta:
        model = Candidate
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
