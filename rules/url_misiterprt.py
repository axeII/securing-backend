"""This is the url misinterpretation module.

So-called directory traversal or path traversal attacks involve modifying the tree structure path in the URL in order to force the server to access unauthorized parts of the site.

The URL (Uniform Resource Locator) of a web application is the vector that makes it possible to indicate the requested resource.
"""
__all__ = ['match_exploit']
__version__ = '0.4'
__author__ = 'Ales Lerch'

from urllib.parse import urlparse
from collections import defaultdict 
from re import match
import logging

logger = logging.getLogger('mainLogger')

def match_exploit(data):
    if isinstance(data,dict):
        try:
            if data['Command'] == 'GET':
                data_specs = [data['Path'],data['Referer'],data['Cookie']] 

                url = urlparse(data_specs[1])
                urlq = url.query
                urlp = url.path

                chars_dict = defaultdict(int)

                for char in urlq:
                    chars_dict[char] = chars_dict[char] + 1

                for key in chars_dict.values():
                    if key >= 4:
                        return True

                if match(r'\/?.\w+',urlp):
                    return True

        except KeyError as k:
            logger.error('Failed to load data_specs from input data:',k)

    return False

if __name__ == "__main__":
    print(match_exploit({'Path':'','Referer': 'http://target/forum/?cat=***********','Cookie':'','Command':'GET'}))
    print(match_exploit({'Path':'','Referer': 'http://target/.bash_history','Cookie':'','Command':'GET'}))
