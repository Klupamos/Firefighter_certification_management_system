from django.db import models

##### TO DO #####
#1. Change ER diagram to allow forign key refence between Jurisdiction and User in terms of TA/CO
#2. Need to intigrate User and Candidate into contrib.auth app
#3. Add permissions (see: https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.permissions)

class Certification(models.Model):
    #not sure need clarification on length 
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
    
class Requirement(models.Model):
    name = models.CharField(max_length=50, unique=True)
    certification = models.ForeignKey(Certification)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
    
class User(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
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
    zip_code = models.CharField(max_length=6)
    state = models.CharField(max_length=20)
    
    jurisdiction = models.ForeignKey('Jurisdiction')
    certifications = models.ManyToManyField(Certification)
    requirements = models.ManyToManyField(Requirement)

    def __unicode__(self):
        return self.firstname + ' '+ self.middle_initial + ' ' + self.last_name + ' ' + self.suffix
    
    class Meta:
        ordering = ["last_name", "first_name"]
    
    
    
class Jurisdiction(models.Model):
    name = models.CharField(max_length=50, unique=True)
    training_officer = models.ManyToManyField(Candidate, related_name='_TO_')
    certifying_officer = models.ManyToManyField(Candidate, related_name='_CO_')

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering  = ["name"]    
    
class Transfer_Request(models.Model):                # candidate wants to move jurisdictions
    candidate    = models.ForeignKey(Candidate)
    jurisdiction = models.ForeignKey(Jurisdiction)
    TO_approval  = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        order_with_respect_to = 'candidate'