import os
osfile = [f for f in os.listdir("database") if f.endswith(".sqlite3")]
os.chdir("database")
for f in osfile:
	os.remove(f)
os.chdir("..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fire_fighter_site.settings")
from django.core import management
management.call_command('syncdb', interactive=False)
from candidate.models import *
# NEED TO CHANGE THIS TO MYSQL WHEN REACH PRODUCTION
# Removes everything ending with sql lite

#get_or_create does a save
req1 = Requirement.objects.get_or_create(name = "Kill 50 chickens")[0]
req2 = Requirement.objects.get_or_create(name = "Kill 50 dolphins")[0]
req3 = Requirement.objects.get_or_create(name = "Kill 50 small animals")[0]
req4 = Requirement.objects.get_or_create(name = "Be my facebook friend")[0]


cert3 = Certification.objects.get_or_create(name = "Completed World of Warcraft Quest", description = "Complete all three requirements for the quest")[0]
cert3.Add_Requirements(req1, req2, req3)
cert3.save()

cert4 = Certification.objects.get_or_create(name = "Become my best friend", description = "Be friendly")[0]
cert4.Add_Requirements(req4)
cert4.save()


j1 = Jurisdiction.objects.get_or_create(name = "Fairbanks")[0]
j2 = Jurisdiction.objects.get_or_create(name = "North pole")[0]
j3 = Jurisdiction.objects.get_or_create(name = "Anchorage")[0]


c1 = Candidate.objects.get_or_create(email_address = "A@B.com", first_name = "Redmond", last_name = "Mann", phone_number = 9074565588, street_address = "quiggly ln", city_name = "Fairbanks", postal_code = 45337, state_abrv = "AK")[0]
c1.set_password("rootpass")
c1.jurisdiction = j1
c1.Request_Jurisdiction_Transfer(j2)
c1.Add_Requirements(req1, req2, req3)
c1.Make_Training_Officer_of(j1, j2)
c1.Make_Certifying_Officer_of(j1, j2)
c1.Make_Administrator()
c1.save()


c2 = Candidate.objects.get_or_create(email_address = "B@C.com", first_name = "Bluetarch", last_name = "Mann", phone_number = 9074565588, street_address = "quiggly ln", city_name = "North pole", postal_code = 45337, state_abrv = "AK")[0]
c2.set_password("moocow")
c2.jurisdiction = j2
c2.Add_Requirements(req4)
c2.save()

from datetime import date
candidate_earned_certification.objects.filter(candidate = c2).update(
    expiration_date = date(
        date.today().year,
        date.today().month,
        28 if date.today().day <= 15 else 1
    )
)
candidate_earned_certification.objects.filter(candidate = c1).update(
    expiration_date = date(
        date.today().year,
        date.today().month,
        28 if date.today().day >= 15 else 1
    )
)


