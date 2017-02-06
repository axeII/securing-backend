"""This is the example module.

Example of rule classificator how should normal exploit rule look like.
"""
__all__ = ['match_exploit']
__version__ = '0.4'
__author__ = 'Ales Lerch'

import logging
logger = logging.getLogger('ruleLogger')
# When writing error use logger to write error etc logger.error,info,warning

# Main function match_exploit
def match_exploit(data):
    if isinstance(data,dict):
        for key,val in data.items(): pass
    # Take data from other class, this data will be in specific format:
    # defaultdict(<class 'list'>,
    #            {'Accept': ['*/*'],
    #             'Accept-Encoding': ['gzip,-deflate'],
    #             'Accept-Language': ['cs-cz'],
    #             'Client_address': ['IP-Address:127.0.0.1,port:59196'],
    #             'Command': ['GET'],
    #             'Connection': ['keep-alive'],
    #             'Cookie': ['SQLiteManager_currentLangue=2'],
    #             'Error': [None],
    #             'Host': ['localhost:8887'],
    #             'If-Modified-Since': ['Thu,-01-Sep-2016-14:59:13-GMT'],
    #             'If-None-Match': ['W/"29c816-1-53b7374f45240"'],
    #             'Path': ['/MAMP/feed/needsUpdate.txt'],
    #             'Referer': ['http://localhost:8887/MAMP/?language=English'],
    #             'Socket_info': ['AddressFamily.AF_INET,SocketKind.SOCK_STREAM,Protocol-Protocol-0'],
    #             'Time': ['2016-09-02_21:14:40'],
    #             'User-Agent': ['Mozilla/5.0-(Macintosh;-Intel-Mac-OS-X-10_11_6)-AppleWebKit/601.7.7-(KHTML,-like-Gecko)-Version/9.1.2-Safari/601.7.7'],
    #             'Version': ['HTTP/1.1'],
    #             'X-Requested-With': ['XMLHttpRequest']})


    return False
    # This function should return True if it finds specific exploit else False
    # Important!! If function doesn't return True or False, it will be
    # considered not working


# If you want to test your module use pythonic way to do it:
if __name__ == "__main__":
    pass
    # All your test

# This example will be updated when changes occur. Last change: {14/09/16}

##############################################
