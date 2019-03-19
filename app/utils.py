import re

def get_route(path, urls):
    '''
        Find a a specific /path and return its callback function.
    '''
    for regex, callback in urls:
        match = re.search(regex, path)
        if match:
            return callback
    return None
