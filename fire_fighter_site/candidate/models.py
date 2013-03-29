from django.db import models

##### TO DO #####
#1. Change ER diagram to allow forign key refence between Jurisdiction and User in terms of TA/CO
#2. Need to intigrate User and Candidate into contrib.auth app

class Certification(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000)
    requirements = models.ManyToManyField('Requirement', related_name='certifications')

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
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        order_with_respect_to = 'candidate'

class Candidate(models.Model):
    fire_fighter_ID = models.CharField(max_length=10, unique=True) #need to add somthing here to make sure that user does not put in an arbitrary FF ID, or make this a foregin key with some kind of look up in the implementation
    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=1, blank=True)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=4, blank=True)
    phone_number = models.IntegerField(max_length=14, blank=True) # (###)-###-#### ext: ####
    email = models.EmailField(blank=True)
    
    #Do not need to validate these three here, see django.contrib.localflavor
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    
    jurisdiction = models.ForeignKey('Jurisdiction', related_name='candidate_list')
    certifications = models.ManyToManyField(Certification, related_name='completed_by+')
    requirements = models.ManyToManyField(Requirement, related_name='completed_by+')

    def __unicode__(self):
        return " ".join([self.first_name, self.middle_initial, self.last_name, self.last_name, self.suffix])
    
    class Meta:
        ordering = ["last_name", "first_name"]
        unique_together = ('first_name','middle_initial','last_name','suffix')
    
    
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
