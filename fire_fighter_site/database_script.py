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


r1 = Requirement(name = "Kill 50 chickens")
r2 = Requirement(name = "Kill 50 dolphins")
r3 = Requirement(name = "Kill 50 small animals")
r4 = Requirement(name = "Be my facebook friends")
r1.save()
r2.save()
r3.save()
r4.save()

c1 = Candidate.objects.get_or_create(email_address = "A@B.com", first_name = "blue", middle_initial = "Q", last_name = "Campell", phone_number = 9074565588, street_address = "quiggly ln", city_name = "Fairbanks", postal_code = 45337, state_abrv = "AK")[0]
c1.set_password("rootpass")
c1.save()

c3 = Certification.objects.get_or_create(name = "Compleated World of Warcraft Quest", description = "Completed all three things requirements for the quest")[0]

c3.Add_Requirement(r1)
c3.Add_Requirement(r2)
c3.Add_Requirement(r3)
c3.save()

c4 = Certification.objects.get_or_create(name = "Become my best friend", description = "Complete requirement 4")[0]
c4.Add_Requirement(r4)
c4.save()




c1 = Candidate.objects.get_or_create(email_address = "B@C.com", first_name = "blue", middle_initial = "Q", last_name = "Campell", phone_number = 9074565588, street_address = "quiggly ln", city_name = "Fairbanks", postal_code = 45337, state_abrv = "AK")[0]
c1.set_password("moocow")
c1.Add_Requirement(r1)
c1.Add_Requirement(r3)
c1.Add_Certification(c4)

c1.save()




