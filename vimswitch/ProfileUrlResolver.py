def getProfileUrl(profile):
    prefix = 'https://github.com/'
    suffix = '/archive/master.zip'
    url = prefix + profile.getName() + suffix
    return url
