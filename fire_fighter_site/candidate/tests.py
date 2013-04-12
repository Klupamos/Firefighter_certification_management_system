"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from models import *


class SimpleTest(TestCase):
    def test_Add_Cert_Without_Req(self):
        c1 = Candidate.objects.get_or_create(email_address = "webmaster@localhost.com", first_name = "Test", last_name = "Candidate", street_address = "123 paved rd", city_name = "anytown", postal_code = 0, state_abrv = "AK")[0]
        
        req1 = Requirement.objects.get_or_create(name = "Link facebook post")[0]
        
        cert1 = Certification.objects.get_or_create(name = "Facebook Friends", description = "Facebook is cool")[0]
        cert1.requirements.add(req1)
        cert1.save()
        
        self.assertQuerysetEqual(c1.earned_certifications.all(), [])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [])
        
        c1.Add_Certification(cert1)

        self.assertQuerysetEqual(c1.earned_certifications.all(), [repr(cert1)])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [repr(req1)])
        
    def test_Add_Cert_With_Req(self):
        c1 = Candidate.objects.get_or_create(email_address = "webmaster@localhost.com", first_name = "Test", last_name = "Candidate", street_address = "123 paved rd", city_name = "anytown", postal_code = 0, state_abrv = "AK")[0]
        
        req1 = Requirement.objects.get_or_create(name = "Link facebook post")[0]
        
        cert1 = Certification.objects.get_or_create(name = "Facebook Friends", description = "Facebook is cool")[0]
        cert1.requirements.add(req1)
        cert1.save()

        self.assertQuerysetEqual(c1.earned_certifications.all(), [])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [])
        
        c1.Add_Requirement(req1)
        c1.Add_Certification(cert1)

        self.assertQuerysetEqual(c1.earned_certifications.all(), [repr(cert1)])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [repr(req1)])

    def test_Add_Req(self):
        c1 = Candidate.objects.get_or_create(email_address = "webmaster@localhost.com", first_name = "Test", last_name = "Candidate", street_address = "123 paved rd", city_name = "anytown", postal_code = 0, state_abrv = "AK")[0]
        
        req1 = Requirement.objects.get_or_create(name = "Link facebook post")[0]

        self.assertQuerysetEqual(c1.earned_requirements.all(), [])
        c1.Add_Requirement(req1)
        self.assertQuerysetEqual(c1.earned_requirements.all(), [repr(req1)])
        
    def tes_Remove_Req(self):
        c1 = Candidate.objects.get_or_create(email_address = "webmaster@localhost.com", first_name = "Test", last_name = "Candidate", street_address = "123 paved rd", city_name = "anytown", postal_code = 0, state_abrv = "AK")[0]
        
        req1 = Requirement.objects.get_or_create(name = "Link facebook post")[0]

        self.assertQuerysetEqual(c1.earned_requirements.all(), [])
        c1.Add_Requirement(req1)
        self.assertQuerysetEqual(c1.earned_requirements.all(), [repr(req1)])
        c1.Revoke_Requirement(req1)
        self.assertQuerysetEqual(c1.earned_requirements.all(), [])
    
    def test_Remove_Cert_And_Req(self):
        c1 = Candidate.objects.get_or_create(email_address = "webmaster@localhost.com", first_name = "Test", last_name = "Candidate", street_address = "123 paved rd", city_name = "anytown", postal_code = 0, state_abrv = "AK")[0]
        
        req1 = Requirement.objects.get_or_create(name = "Link facebook post")[0]
        
        cert1 = Certification.objects.get_or_create(name = "Facebook Friends", description = "Facebook is cool")[0]
        cert1.requirements.add(req1)
        cert1.save()

        
        c1.Add_Certification(cert1)
        self.assertQuerysetEqual(c1.earned_certifications.all(), [repr(cert1)])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [repr(req1)])
        c1.Revoke_Certification(cert1, True)
        self.assertQuerysetEqual(c1.earned_certifications.all(), [])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [])       
        
    def test_Remove_Cert_Not_Req(self):
        c1 = Candidate.objects.get_or_create(email_address = "webmaster@localhost.com", first_name = "Test", last_name = "Candidate", street_address = "123 paved rd", city_name = "anytown", postal_code = 0, state_abrv = "AK")[0]
        
        req1 = Requirement.objects.get_or_create(name = "Link facebook post")[0]
        
        cert1 = Certification.objects.get_or_create(name = "Facebook Friends", description = "Facebook is cool")[0]
        cert1.requirements.add(req1)
        cert1.save()

        
        c1.Add_Certification(cert1)
        self.assertQuerysetEqual(c1.earned_certifications.all(), [repr(cert1)])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [repr(req1)])
        c1.Revoke_Certification(cert1, False)
        self.assertQuerysetEqual(c1.earned_certifications.all(), [])
        self.assertQuerysetEqual(c1.earned_requirements.all(), [repr(req1)])