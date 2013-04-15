from django.test import TestCase
from models import *     

class Certification_Tests(TestCase):
    def setUp(self):
        self.reqs = []
        for i in range(3):
            req = Requirement.objects.create(name = "Requirement: "+str(i))
            self.reqs.append(req)
            
        self.certs = []
        for i in range(3):
            cert = Certification.objects.create(name = "Certification: "+str(i), description = "Empty")
            self.certs.append(cert)
        
        self.certs[2].requirements.add(*self.reqs)
        self.certs[2].save()
          
        self.jurs = []
        for i in range(3):
            jur= Jurisdiction.objects.create(name=str(i))
            self.jurs.append(jur)
        
        self.cands = []
        for i in range(3):
            cand = Candidate.objects.create(email_address = "web"+str(i)+"@localhost.com", last_name=str(i), first_name=str(i))
            cand.jurisdiction = self.jurs[2]
            cand.Add_Requirements(*self.reqs)
            cand.save()
            self.cands.append(cand)
        
        
    def test_Add_Requirement(self):
        self.certs[0].Add_Requirements(self.reqs[0])
        self.assertTrue(self.reqs[0] in self.certs[0].requirements.all())
    
    def test_Add_Unique_Requirements(self):
        self.certs[0].Add_Requirements(self.reqs[0], self.reqs[1])
        A = set(self.certs[0].requirements.all())
        B = set([self.reqs[0], self.reqs[1]])
        self.assertEqual(A.difference(B), set())
    
    def test_Add_Duplicate_Requirements(self):
        self.certs[0].Add_Requirements(self.reqs[0], self.reqs[0])
        A = set(self.certs[0].requirements.all())
        B = set([self.reqs[0], self.reqs[0]])
        self.assertEqual(A.difference(B), set())
    
    def test_Remove_Requirement(self):
        self.certs[0].requirements.add(self.reqs[0])
        self.certs[0].Remove_Requirements(self.reqs[0])
        A = [x for x in self.certs[0].requirements.all()]
        B = []
        self.assertEqual(A, B)
    
    def test_Remove_Unique_Requirements(self):
        self.certs[0].requirements.add(self.reqs[0], self.reqs[1])
        self.certs[0].Remove_Requirements(self.reqs[0], self.reqs[1])
        A = [x for x in self.certs[0].requirements.all()]
        B = []
        self.assertEqual(A, B)
    
    def test_Remove_Duplicate_Requirements(self):
        self.certs[0].requirements.add(self.reqs[0], self.reqs[0])
        self.certs[0].Remove_Requirements(self.reqs[0], self.reqs[0])
        A = [x for x in self.certs[0].requirements.all()]
        B = []
        self.assertEqual(A, B)
    
    def test_Remove_Nonrequired_Requirements(self):
        self.certs[0].requirements.add(self.reqs[0], self.reqs[1])
        self.certs[0].Remove_Requirements(self.reqs[0])
        A = [x for x in self.certs[0].requirements.all()]
        B = [self.reqs[1]]
        self.assertEqual(A, B)
        
    def test_Add_Certification(self):
        self.certs[0].Add_Certifications(self.certs[1])
        A = [x for x in self.certs[0].certifications.all()]
        B = [self.certs[1]]
        self.assertEqual(A, B)
        
    def test_Add_Self_Certification(self):
        self.certs[0].Add_Certifications(self.certs[0])
        A = [x for x in self.certs[0].certifications.all()]
        B = []
        self.assertEqual(A, B)
    
    def test_Add_Unique_Certifications(self):
        self.certs[0].Add_Certifications(self.certs[1], self.certs[2])
        A = [x for x in self.certs[0].certifications.all()]
        B = [self.certs[1], self.certs[2]]
        self.assertEqual(A, B)
    
    def test_Add_Duplicate_Certifications(self):
        self.certs[0].Add_Certifications(self.certs[1], self.certs[1])
        A = [x for x in self.certs[0].certifications.all()]
        B = [self.certs[1]]
        self.assertEqual(A, B)
    
    def test_Remove_Certification(self):
        self.certs[0].certifications.add(self.certs[1])
        self.certs[0].Remove_Certifications(self.certs[1])
        A = [x for x in self.certs[0].certifications.all()]
        B = []
        self.assertEqual(A, B)
    
    def test_Remove_Unique_Certifications(self):
        self.certs[0].certifications.add(self.certs[1], self.certs[2])
        self.certs[0].Remove_Certifications(self.certs[1])
        A = [x for x in self.certs[0].certifications.all()]
        B = [self.certs[2]]
        self.assertEqual(A, B)
    
    def test_Remove_Duplicate_Certifications(self):
        self.certs[0].certifications.add(self.certs[1], self.certs[2])
        self.certs[0].Remove_Certifications(self.certs[1], self.certs[1])
        A = [x for x in self.certs[0].certifications.all()]
        B = [self.certs[2]]
        self.assertEqual(A, B)
    
    def test_Remove_Nonrequired_Certifications(self):
        self.certs[0].certifications.add(self.certs[1])
        self.certs[0].Remove_Certifications(self.certs[2])
        A = [x for x in self.certs[0].certifications.all()]
        B = [self.certs[1]]
        self.assertEqual(A, B)
        
    def test_is_Deprecate(self):
        self.certs[0].deprecated = True
        self.assertEqual(self.certs[0].Is_Deprecated(), True)
        
    def test_Deprecate(self):
        self.certs[0].Deprecate(True)
        self.assertEqual(self.certs[0].deprecated, True)

    def test_Eligible_Candidates_List(self):
        q_set = [ x for x in self.jurs[2].Eligible_Candidates_List()]
        empty = []
        self.assertEqual(q_set, empty)
        
    def test_Eligible_Candidates_List(self):
        q_set = [ x for x in self.jurs[2].Eligible_Candidates_List(self.certs[2])]
        self.assertEqual(q_set, self.cands)        
        
class Candidate_Test(TestCase):
    def test_implement(self):
        pass

class Jurisdiction_Test(TestCase):
    def setUp(self):
        self.cand = []
        for i in range(5):
            c = Candidate.objects.create(email_address = "webmaster"+str(i)+"@localhost.com", first_name = str(i), last_name = str(i))
            self.cand.append(c)
            
        self.jur = []
        for i in range(5):
            j = Jurisdiction.objects.create(name = "Jurisdiction: "+str(i))
            self.jur.append(j)
        
    def test_Appoint_Training_Officers(self):
        self.jur[0].Appoint_Training_Officers(self.cand[0])
        A = [x for x in self.jur[0].training_officer.all()]
        B = [self.cand[0]]
        self.assertEqual(A, B)
        
    def test_Revoke_Training_Officers(self):
        self.jur[0].training_officer.add(self.cand[0])
        self.jur[0].Revoke_Training_Officers(self.cand[0])
        A = [x for x in self.jur[0].training_officer.all()]
        B = []
        self.assertEqual(A, B)
        
    def test_Appoint_Certifying_Officers(self):
        self.jur[0].Appoint_Certifying_Officers(self.cand[0])
        A = [x for x in self.jur[0].certifying_officer.all()]
        B = [self.cand[0]]
        self.assertEqual(A, B)
        
    def test_Revoke_Certifying_Officers(self):
        self.jur[0].certifying_officer.add(self.cand[0])
        self.jur[0].Revoke_Certifying_Officers(self.cand[0])
        A = [x for x in self.jur[0].certifying_officer.all()]
        B = []
        self.assertEqual(A, B)
   
class Transfer_Request_Test(TestCase):
    def setUp(self):
        cand = []
        for i in range(5):
            c = Candidate.objects.create(email_address = "webmaster"+str(i)+"@localhost.com", first_name = str(i), last_name = str(i))
            cand.append(c)
        
        jur = []
        for i in range(5):
            j = Jurisdiction.objects.create(name = "Jurisdiction: "+str(i))
            jur.append(j)
        
        self.tr = Transfer_Request.objects.create(candidate = cand[0], jurisdiction = jur[0])
        
    def test_Positive_Training_Approval(self):
        self.tr.Training_Approval(True)
        A = [x for x in Transfer_Request.objects.filter(candidate = self.tr.candidate, jurisdiction = self.tr.jurisdiction)]
        B = [self.tr]
        self.assertEqual(A, B) # request exists
        self.assertEqual(self.tr.TO_approval, True)

    def test_Negative_Training_Approval(self):
        self.tr.Training_Approval(False)
        A = [x for x in Transfer_Request.objects.filter(candidate = self.tr.candidate, jurisdiction = self.tr.jurisdiction)]
        B = []
        self.assertEqual(A, B) # request deleted
        
    def test_Positive_Admin_Approval(self):
        self.tr.Admin_Approval(True)
        A = [x for x in Transfer_Request.objects.filter(candidate = self.tr.candidate, jurisdiction = self.tr.jurisdiction)]
        B = []
        self.assertEqual(A, B) # request deleted

    def test_Negative_Admin_Approval(self):
        self.tr.Admin_Approval(False)
        A = [x for x in Transfer_Request.objects.filter(candidate = self.tr.candidate, jurisdiction = self.tr.jurisdiction)]
        B = []
        self.assertEqual(A, B) # request deleted

from datetime import date, timedelta
class CEC_Test(TestCase):
    def setUp(self):
        self.cand = Candidate.objects.create(email_address = "webmaster@localhost.com", first_name = "f", last_name = "l")
        self.cert = Certification.objects.create(name = "cert")
        
    def test_candidate_earned_certification_save(self):
        months = 9*12 + 11
        cec = candidate_earned_certification.objects.create(candidate = self.cand, certification = self.cert)
        cec.update(months_valid = months)
        
        lazy_lower_limit = timedelta(days = (months/12) * 365 + (months%12) * 28)
        lazy_upper_limit = timedelta(days = (months/12) * 366 + (months%12) * 31)
        
        self.assertEqual(cec.date, date.today())
        self.assertNotEqual(cec.expiration_date, cec.date)
        self.assertNotEqual(cec.expiration_date, None)
        self.assertGreaterEqual(cec.expiration_date - cec.date, lazy_lower_limit)
        self.assertLessEqual(cec.expiration_date - cec.date, lazy_upper_limit)
        print str(lazy_lower_limit) + " <= " + str(cec.expiration_date - cec.date) + " <= " + str(lazy_upper_limit)

class CER_Test(TestCase):
    def setUp(self):
        pass