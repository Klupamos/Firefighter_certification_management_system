import ConfigParser
from django.conf import settings

class anchor(object):
    def __init__(self, text, href):
        self.href = href
        self.text = text

def create_navlinks(user):
    config = ConfigParser.RawConfigParser()
    config.read(settings.CONFIG_FILE)
    
    nav_links = []
    
    if user.is_authenticated():
        for a in config.items('Candidate URLs'):
            nav_links.append(anchor(a[0], a[1]))
                
        if user.Is_Authorized('TO'):
            for a in config.items('Training Officer URLs'):
                nav_links.append(anchor(a[0], a[1]))
        if user.Is_Authorized('CO'):
            for a in config.items('Certifying Officer URLs'):
                nav_links.append(anchor(a[0], a[1]))
        if user.Is_Authorized('AD'):
            for a in config.items('Administration URLs'):
                nav_links.append(anchor(a[0], a[1]))
    else:
        for a in config.items('Anonymous URLs'):
            nav_links.append(anchor(a[0], a[1]))
    
    for a in config.items('Everyone URLs'):
        nav_links.append(anchor(a[0], a[1]))
    return nav_links