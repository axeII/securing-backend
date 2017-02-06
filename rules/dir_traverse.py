"""This is the directory traversal module.

A path traversal attack (also known as directory traversal) aims to access files and directories that are stored outside the web root folder. By manipulating variables that reference files with “dot-dot-slash (../)” sequences and its variations or by using absolute file paths, it may be possible to access arbitrary files and directories stored on file system including application source code or configuration and critical system files. It should be noted that access to files is limited by system operational access control.

This attack is also known as “dot-dot-slash”, “directory traversal”, “directory climbing” and “backtracking”.
"""
__all__ = ['match_exploit']
__version__ = '0.6'
__author__ = 'Ales Lerch'

from urllib.parse import urlparse
from re import match
import logging

logger = logging.getLogger('mainLogger')

def match_exploit(data):
    if isinstance(data,dict):
        try:
            if data['Command'] == 'GET':
                specific_chars = [
                        '%2e%2e/','..%2f','../'
                        ]
                data_specs = [
                        data['Path'],data['Referer'],data['Cookie']
                        ]
                for data in data_specs:
                    n_times = []
                    for spec in specific_chars:
                        n_times.append(data.find(spec))

                    for ch,n in zip(specific_chars,n_times):
                        if n > -1:
                            culprit = ch
                            return True

                parse_data = data_specs[1]
                if parse_data:
                    u = urlparse(data_specs[1]).query
                    if 'http' in u or 'https' in u:
                        return True
                    if match(r'[a-z]+=[a-z]+.[a-z]{3}',u) or match(r'[a-z/]+',u):
                        return True

        except KeyError as k:
            logger.error('Failed to load data_specs from input data:',k)

    return False

if __name__ == "__main__":
    print(match_exploit({'Path':'/MAMP/feed/needsUpdate.txt','Referer': 'http://localhost:8887/MAMP/?language=English','Cookie':'','Command':'GET'}))
    print(match_exploit({'Path':'/MAMP/feed/needsUpdate.txt','Referer': 'http://some_site.com.br/some-page?page=http://other-site.com.br/other-page.htm/malicius-code.php','Cookie':'','Command':'GET'}))
    print(match_exploit({'Path':'/MAMP/feed/needsUpdate.txt','Referer': 'http://vulnerable-page.org/cgi-bin/main.cgi?file=main.cgi','Cookie':'','Command':'GET'}))
    print(match_exploit({'Path':'/MAMP/feed/needsUpdate.txt','Referer': 'http://test.webarticles.com/show.asp?view=../../../../../Windows/system.ini','Cookie':'','Command':'GET'}))
