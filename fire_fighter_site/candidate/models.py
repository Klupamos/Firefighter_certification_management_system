from django.db import models
from django.conf import settings

##### TO DO #####
#1. Change ER diagram to allow forign key refence between Jurisdiction and User in terms of TA/CO
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


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
class CandidateManager(BaseUserManager):
    def create_user(self, username, password, firstname, lastname, street, city, postal, state):
        if not username:
            raise ValueError('User must have a username')
           
        user = self.model(
            user_name = username,
            first_name = firstname,
            last_name = lastname,
            street_address = street,
            city_name = city,
            postal_code = postal,
            state_abrv = state,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, **kwargs):
        user = self.create_user(
            username  = kwargs['user_name'],
            password  = kwargs['password'],
            firstname = kwargs['first_name'],
            lastname  = kwargs['last_name'],
            street    = kwargs['street_address'],
            city      = kwargs['city_name'],
            postal    = kwargs['postal_code'],
            state     = kwargs['state_abrv']
        )
        user.administrator_approved = True
        user.appoint_as_administrator()
        user.save(using=self._db)
        return user
 
from django.core.exceptions import ObjectDoesNotExist
class Candidate(AbstractBaseUser):
    # authentication
    email_address = models.EmailField(max_length=254, unique=True, db_index=True)
    #password added by AbstractBaseUSer
    
    # name
    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=1, blank=True, default='')
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=4, blank=True, default='')

    # contact
    phone_number = models.IntegerField(max_length=14, null=True) # (###)-###-#### ext: ####
    street_address = models.CharField(max_length=50)
    city_name = models.CharField(max_length=25)
    postal_code = models.CharField(max_length=10)
    state_abrv = models.CharField(max_length=20, default='AK')

    #foreign keys
    jurisdiction = models.ForeignKey('Jurisdiction', related_name='candidate_list', null=True)
    processing_certifications = models.ManyToManyField(Certification, through='certification_processing')
    earned_certifications = models.ManyToManyField(Certification, through='candidate_earned_certification')
    earned_requirements = models.ManyToManyField(Requirement, through='candidate_earned_requirement')

    #required by AbstractBaseUser class
    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'street_address', 'city_name', 'postal_code', 'state_abrv']
    is_active = models.BooleanField(default=True)
    administrator_approved = models.BooleanField(default=False)
    objects = CandidateManager()

    class Meta:
        ordering = ["last_name", "first_name"]
        unique_together = ('first_name','middle_initial','last_name','suffix')
        
    def get_full_name(self): # defined in AbstractBaseUser
        return " ".join(filter(None, (self.first_name, self.middle_initial, self.last_name, self.suffix)))
    
    def get_short_name(self): # defined in AbstractBaseUser
        return self.first_name
        
    def get_firefighter_id(self):
        return self.last_name[0:4].upper() + str(self.id).zfill(4)[-4:]
    
    def __unicode__(self):
        return self.get_firefighter_id()
    
    def is_training_officer(self):
        if self.trains_jurisdiction.all():
            return True
        else:
            return False
            
    def is_certifying_officer(self):
        if self.certifies_jurisdiction.all():
            return True
        else:
            return False
            
    def is_administrator(self):
        try:
            admin = Administrators.objects.get(candidate = self)
            return True
        except ObjectDoesNotExist:
            return False
            
    def appoint_as_administrator(self):
        admin = Administrators.objects.get_or_create(candidate = self)
        
    def revoke_administrator(self):
        raise NotImplementedError()

class certification_processing(models.Model):
    candidate = models.ForeignKey(Candidate, primary_key=True)
    certification = models.ForeignKey(Certification)
    
        
class candidate_earned_certification(models.Model):
    candidate = models.ForeignKey(Candidate, primary_key=True)
    certification = models.ForeignKey(Certification)
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

    class Meta:
        ordering  = ["name"] 
        
    def __unicode__(self):
        return self.name   
    
    def appoint_training_officer(self, candidate):
        raise NotImplementedError()
        
    def revoke_training_officer(self, candidate):
        raise NotImplementedError()
        
    def appoint_certifying_officer(self, candidate):
        raise NotImplementedError()
        
    def revoke_certifying_officer(self, candidate):
        raise NotImplementedError()

        
class Transfer_Request(models.Model):
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='requested_transfers', primary_key=True)
    candidate    = models.ForeignKey(Candidate, related_name='transfer_request', unique=True)
    TO_approval  = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        order_with_respect_to = 'candidate'


class Administrators(models.Model):
    candidate = models.ForeignKey(Candidate, primary_key=True, unique=True)
