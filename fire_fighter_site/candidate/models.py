from django.db import models
from django.conf import settings

# for Candidate.(Add/Remove)_(Certification/Requirement)
from django.db.models import Q
from operator import __or__

##### TO DO #####
#1. Change ER diagram to allow forign key refence between Jurisdiction and User in terms of TA/CO


class Certification(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000)
    requirements = models.ManyToManyField('Requirement', related_name='certifications')
    certifications = models.ManyToManyField("self")
    months_valid = models.IntegerField(default=0) #number of months this certification is valid. 0 for never
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        
    def Add_Requirements(self, *req_list):
        print self, " adding: ", req_list
        self.requirements.add(*req_list)
        self.save()

    def Add_Certifications(self, *cert_list):
        print self, " adding: ", cert_list
        cert_list.remove(self)
        self.requirements.add(*cert_list)
        self.save()
        
class Requirement(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
class CandidateManager(BaseUserManager):
    def create_user(self, email_address, password, firstname, lastname, street, city, postal, state):
        if not email_address:
            raise ValueError('User must have a username')
           
        user = self.model(
            email_address = email_address,
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
            email_address  = kwargs['email_address'],
            password  = kwargs['password'],
            firstname = kwargs['first_name'],
            lastname  = kwargs['last_name'],
            street    = kwargs['street_address'],
            city      = kwargs['city_name'],
            postal    = kwargs['postal_code'],
            state     = kwargs['state_abrv']
        )
        user.administrator_approved = True
        user.Appoint_As_Administrator()
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
        #unique_together = ('first_name','middle_initial','last_name','suffix')
    
#class methods
    def get_full_name(self): # defined in AbstractBaseUser
        return " ".join(filter(None, (self.first_name, self.middle_initial, self.last_name, self.suffix)))
    
    def get_short_name(self): # defined in AbstractBaseUser
        return self.first_name
        
    def get_firefighter_id(self):
        return self.last_name[0:4].upper() + str(self.id).zfill(4)[-4:]
    
    def __unicode__(self):
        return self.get_firefighter_id()
    
    def Login(self):
        raise 0
        
    def logout(self):
        raise 0
    
    def Is_Authorized(self, permission_lvl):
        perms = {}
        perms['CD'] = lambda : self.Is_Candidate()
        perms['TO'] = lambda : self.Is_Training_Officer()
        perms['CO'] = lambda : self.Is_Certifying_Officer()
        perms['AD'] = lambda : self.Is_Administrator()
        try:
            return perms[permission_lvl]()
        except:
            return False
            
    def Update_Fields(self, **fields):
        raise 0

    def Make_Candidate(self):
        self.administrator_approved = True
        
    def Retire_Candidate(self):
        self.administrator_approved = False
        
    def Is_Candidate(self):
        return self.administrator_approved
    
    def Make_Training_Officer_of(self, jurisdiction):
        jurisdiction.training_officer.add(self)
        
    def Retire_as_Training_Officer_of(self, jurisdiction):
        jurisdiction.training_officer.remove(self)
    
    def Is_Training_Officer(self):
        if self.trains_jurisdiction.all():
            return True
        else:
            return False    
    
    def Make_Certifying_Officer_of(self, jurisdiction):
        jurisdiction.training_officer.add(self)
        
    def Retire_Certifying_Officer_of(self, jurisdiction):
        jurisdiction.training_officer.remove(self)
        
    def Is_Certifying_Officer(self):
        if self.certifies_jurisdiction.all():
            return True
        else:
            return False
    
    def Make_Administrator(self):
        admin = Administrators.objects.get_or_create(candidate = self)[0]
        
    def Retire_Administrator(self):
        try:
            Administrators.objects.get(candidate = self).delete()
        except ObjectDoesNotExist:
            pass

    def Is_Administrator(self):
        try:
            admin = Administrators.objects.get(candidate = self)
            return True
        except ObjectDoesNotExist:
            return False
        
    def Request_Jurisdiction_Transfer(self, jurisdiction):
        tr = Transfer_Request.objects.get_or_create(candidate = self)[0]
        tr.jurisdiction = jurisdiction
        tr.TO_approval = False
        tr.save()
        
    def Add_Requirements(self, *req_list):
        if not req_list:
            return
        req_list = set(req_list)
        print self, " adding: ", req_list
        for req in req_list:
            candidate_earned_requirement.objects.get_or_create(candidate = self, requirement = req)
        
    def Remove_Requirements(self, *req_list, **kargs):
        if not req_list:
            return
        req_list = set(req_list)
        print self, " removing: ", req_list
        
        super_cert_list = set()
        Q_filter = []
        for req in req_list:
            super_cert_list.update(req.certifications.all())
            
            Q_filter.append(Q(candidate = self, requirement = req))
        
        delete_list = candidate_earned_requirement.objects.filter(reduce(__or__, Q_filter))
        
        if kargs.get('bubble',True):
            # I should also remove any Certifications that rely on these
            self.Remove_Certifications(*super_cert_list)
        
        delete_list.delete()
        
    def List_Requirements(self):
        return Requirement.objects.filter(candidate = self)
        
    def Add_Certifications(self, *cert_list, **cert_key_words):
        if not cert_list:
            return
        cert_list = set(cert_list)
        print self, " adding: ", cert_list
        sub_req_list = set()
        sub_cert_list = set()
        for cert in cert_list:
            cert_obj = candidate_earned_certification.objects.get_or_create(candidate = self, certification = cert)
            if cert_obj[1] and cert_key_words:
                cert_obj[0].expiration_date = cert_key_words.get('expiration_date',None)
                cert_obj[0].IFSAC_date =    cert_key_words.get('IFSAC_date',None)
                cert_obj[0].IFSAC_number =  cert_key_words.get('IFSAC_number',None)
                cert_obj[0].PRO_date =      cert_key_words.get('PRO_date',None)
                cert_obj[0].PRO_number =    cert_key_words.get('PRO_number',None)
                cert_obj[0].company =       cert_key_words.get('company',None)
                cert_obj[0].save()
                
            sub_req_list.update(cert.requirements.all())
            sub_cert_list.update(cert.certifications.all())
                
        self.Add_Certifications(*sub_cert_list)
        self.Add_Requirements(*sub_req_list)
        
    def Remove_Certifications(self, *cert_list, **kargs):
        if not cert_list:
            return
        cert_list = set(cert_list)
        print self, "removing: ", cert_list
        
        super_cert_list = set()
        Q_filter = []
        sub_req_list = set()
        sub_cert_list = set()
        for cert in cert_list:
            super_cert_list.update(cert.certifications.all())
            Q_filter.append(Q(candidate = self, certification = cert))
        
        delete_list = candidate_earned_certification.objects.filter(reduce(__or__, Q_filter))
        
        if kargs.get('cascade',False):
            # I should Remove all requirements and certifications that make up the passed certifications

            for ec in delete_list:
                # Tally up requirements
                sub_req_list.update(ec.certification.requirements.all())
                
                # Tally up sub_certs
                sub_cert_list.update(ec.certification.certifications.all())
                

                
        if kargs.get('bubble',True):
            # I should also remove any Certifications that rely on these
            self.Remove_Certifications(*super_cert_list)
            
        
        # what is the best order to do this in?
        delete_list.delete()
        
        if sub_cert_list:
            self.Remove_Certifications(*sub_cert_list, cascade=True)
        
        if sub_req_list:
            self.Remove_Requirements(*sub_req_list, bubble=kargs.get('bubble',True))

    def List_Certifications(self):
        return Certification.objects.filter(candidate = self)
        
class candidate_earned_certification(models.Model):
    candidate = models.ForeignKey(Candidate) 
    certification = models.ForeignKey(Certification)
    date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True)
    # don't know how many of these are necessary
    IFSAC_date = models.DateField(null=True)
    IFSAC_number = models.IntegerField(null=True)
    PRO_date = models.DateField(null=True)
    PRO_number = models.IntegerField(null=True)
    company = models.CharField(max_length=20)
    
class candidate_earned_requirement(models.Model):
    candidate = models.ForeignKey(Candidate)
    requirement = models.ForeignKey(Requirement)
    date = models.DateField(auto_now_add=True)
        
class Jurisdiction(models.Model):
    name = models.CharField(max_length=50, unique=True)
    training_officer = models.ManyToManyField(Candidate, related_name='trains_jurisdiction')
    certifying_officer = models.ManyToManyField(Candidate, related_name='certifies_jurisdiction')

    class Meta:
        ordering  = ["name"] 
        
    def __unicode__(self):
        return self.name   
    
#class methods    
    def appoint_training_officer(self, candidate):
        self.training_officer.add(candidate)
        
    def revoke_training_officer(self, candidate):
        self.training_officer.remove(candidate)
        
    def appoint_certifying_officer(self, candidate):
        self.certifying_officer.add(candidate)
        
    def revoke_certifying_officer(self, candidate):
        self.certifying_officer.remove(candidate)

class Transfer_Request(models.Model):
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='requested_transfers', primary_key=True)
    candidate    = models.ForeignKey(Candidate, related_name='transfer_request', unique=True)
    TO_approval  = models.BooleanField(default=False)

    def __unicode__(self):
        return str(candidate) + " => " + str(jurisdiction) 
    
    class Meta:
        order_with_respect_to = 'candidate'

#class methods
    def Accept(self):
        self.TO_approval = True
        self.save()
    
    def Reject(slef):
        raise 0
    
    def Approve(self):
        self.candidate.jurisdiction = self.jurisdiction
        self.delete()

    def Disapprove(self):
        raise 0
        
class Administrators(models.Model):
    candidate = models.ForeignKey(Candidate, primary_key=True, unique=True)
