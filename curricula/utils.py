from django.conf import settings
from BeautifulSoup import BeautifulSoup

def truncate(string, limit=44):
    return string[:limit] + (string[limit:] and '...')

def ul_as_list(html):
    soup = BeautifulSoup(html)
    return [li.contents[0] for li in soup('li')]

def get_audience_index(key):
    for i in range(1, 6):
        if settings.AUDIENCE_SETTINGS['AUDIENCE_TYPES'][i]['name'] == key:
            return i
    return 0

def get_audience_indices(items):
    return [get_audience_index(item[0]) for item in items if item[1]]
