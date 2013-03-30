from django.db import models

###TO DO###

#1. Change ER diagram to allow forign key refence between Jurisdiction and User in terms of TA/CO
#2 Add foregin key lookups in Jurisdiction
#3 Add a many to many (m:n) relattionship between requirements and users
#(aka a user can have many requirements and a requirement can be earned by many users)
#4 Add a many to many (m:n) relationship between certifcates and requirements
#(aka a certificate can have many requirements and a requirement can belong to many certifcates)
#5 Add a one to many (1:m) relationship between users and jursidctions 
#(a user may belong to one jursidction but one jursidiction can have many users)
#6 Add a many to many relationship between requirements and Users
#7 There are mutlitple refences to foregin key lookups figure out a way to look up by ID but store by name instead of ID



class User(models.Model):
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	city = models.CharField(max_length = 25)
	#Do not need to validate these three here, see django.contrib.localflavor
	zip_code = models.CharField(max_length = 6)
	state = models.CharField(max_length = 20)
	phone_number = CharField(max_length = 10)
	fire_fighter_ID = CharField(max_length = 50, primary_key = True)
	#need to add somthing here to make sure that user does not put in an arbitrary FF ID, or make this a foregin key with some kind of look up in the implementation
	fire_dept = CharField(max_length = 50)
	email = EmailField()i
	
class Jurisdiction(models.Model):
	jurisdiction_ID = CharField(max_length = 8, primary_key = True)
	name = CharField(max_length = 50)
	#these two I need to add a foregin key refence to User

class Certificate(models.Model):
	#not sure need clarification on length 
	certificate_ID = CharField(max_length = 8, primary_key = True)
	name = CharField(max_length = 50)
	description = charField(max_length = 1000)

class Requirements(models.Model):
	requirement_ID = CharField(max_length = 5, primary_key = True)
	description = CharField(max_length = 500)



