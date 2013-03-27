class anchor(object):
    def __init__(self, href, text):
        self.href = href
        self.text = text

def create_navlinks(user):
    nav_links = []
    # Note these hardcoded if statments need to be changed out for permissions
    if user.is_authenticated():
        nav_links.append(anchor("/account_info","Account Information"))
        nav_links.append(anchor("/account_certs", "Account Certificates"))
        if user.username == 'train':
            nav_links.append(anchor("/training", "Training Officer"))
        if user.username == 'certify':
            nav_links.append(anchor("/certifying", "Certifying Officer"))
        if user.username == 'admin':
            nav_links.append(anchor("/admin", "Administration"))
        nav_links.append(anchor("/public_certs", "view certificates"))
        nav_links.append(anchor("/logout", "logout"))
    else:
        nav_links.extend([anchor("/login", "login"), anchor("/create", "create account"), anchor("/public_certs", "view certificates")])
    return nav_links
