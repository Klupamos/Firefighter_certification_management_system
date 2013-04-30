import ConfigParser
from django.conf import settings 

settings.configure()
config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('Database')
config.set('Database', 'Name', 'test.db')
config.set('Database', 'User', 'testuser')
config.set('Database', 'Pass', 'testpass')
config.set('Database', 'Host', 'localhost')
config.set('Database', 'Port', '8080')


config.add_section('Other')
config.set('Other','Debug','1')
config.set('Other','TimeZone', 'America/Anchorage')
config.set('Other','Site_ID','1')
config.set('Other','Secret_key','86c*_=^%(56-ur2$$ov1fn7)b$5sjg&hz8q5ki!%efdn9_8') # should this be rand()



config.add_section('Anonymous URLs')
config.set('Anonymous URLs', 'Login', '/account/login')
config.set('Anonymous URLs', 'Account Registration', '/account/registration')

config.add_section('Candidate URLs')
config.set('Candidate URLs', 'Logout','/account/logout')
config.set('Candidate URLs', 'Account Information', '/account/modification')

config.add_section('Training Officer URLs')
config.set('Training Officer URLs', 'Training Officer', '/training/display')

config.add_section('Certifying Officer URLs')
config.set('Certifying Officer URLs', 'Certifying Officer', '/certifying/display')

config.add_section('Administration URLs')
config.set('Administration URLs', 'Definitions', '/administrator/definition')

config.add_section('Everyone URLs')
config.set('Everyone URLs', 'View Certificates', '/certifications')

# Writing our configuration file to 'example.cfg'
with open(settings.CONFIG_FILE, 'wb') as configfile:
    config.write(configfile)
