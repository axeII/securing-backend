"""HTTPRequest is module to handle binary http request

then after parsing data puts them into dict and return to previous module.
"""
__author__ = "Ales Lerch"

from http.server import BaseHTTPRequestHandler
from collections import defaultdict
from datetime import datetime
from geolite2 import geolite2
from io import BytesIO
import logging
import pprint
import random
import socket
import struct

class HTTPRequest(BaseHTTPRequestHandler):

    def __init__(self, http_request, client, address,fakeData):
        self.rfile = BytesIO(http_request)
        self.raw_requestline = self.rfile.readline()
        self.data = defaultdict(list)
        self.error_message = None
        self.error_code = None
        self.client = client
        self.address = address
        self.log = logging.getLogger('mainLogger')
        self.fake = fakeData

        try:
            self.parse_request()
        except Exception as e:
            self.log.error('Failed to parse request,reason:%s' % e)

    def get_date_time(self):
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        return (date,time)

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

    def get_info_data(self):

        if self.fake:
            p = ['GET','POST']
            self.data['ip'] = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            self.data['date'] = datetime(random.randint(2014,2016),random.randint(1,12),random.randint(1,28)).strftime("%Y-%m-%d")
            self.data['command'] = p[random.randint(0,1)]
        else:
            self.data['command'] = [self.command]
            self.data['date'] = self.get_date_time()[0]
            self.data['ip'] = str(self.address[0])

        try:
            reader = geolite2.reader()
            self.data['country'] = reader.get(self.data['ip'])['country']['iso_code']
            geolite2.close()
        except TypeError:
            self.data['country'] = "Unknown"

        self.data['socket_info'] = ["%s,%s,Protocol %s" % (self.client.family,self.client.type,self.client.proto)]
        self.data['port'] = str(self.address[1])
        self.data['error'] = [str(self.error_code)]
        self.data['path'] = [self.path]
        self.data['version'] = [self.request_version]
        self.data['time'] = self.get_date_time()[1]
        for key,val in self.headers.items():
            self.data[key].append(val)

        # return parsed data
        return self.data

    def get_data(self):
        self.get_info_data()
        def chef_data(data):
            return ''.join(data) if len(data) <= 1 else data

        for key_, val_ in self.data.items():
            if '-' in key_:
                self.data[str(key_).replace('-','_').lower()] = chef_data(self.data.pop(key_))
            else:
                self.data[str(key_).lower()] = chef_data(self.data.pop(key_))
        return self.data

    def print_data(self):
        self.get_data()
        #p_data = {}
        #for key, data in self.data.items():
        #    if not None in data:
        #        p_data[key] = ''.join(data).replace(' ','-')
        #    else:
        #        p_data[key] = data
        #pprint.pprint(p_data, width=1)
        #print(p_data)
        print(self.data)
        #print(', '.join(["'%s': True" % x for x in self.data.keys()]))
        #for key,val in self.data.items():
        #    print("%s --> %s "%(key,val))

if __name__ == "__main__":
    data = b'GET /MAMP/feed/needsUpdate.txt HTTP/1.1\r\nHost: localhost:8887\r\nAccept-Encoding: gzip, deflate\r\nCookie: SQLiteManager_currentLangue=2\r\nConnection: keep-alive\r\nIf-None-Match: W/"29c816-1-53b7374f45240"\r\nAccept: */*\r\nIf-Modified-Since: Thu, 01 Sep 2016 14:59:13 GMT\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7\r\nReferer: http://localhost:8887/MAMP/?language=English\r\nAccept-Language: cs-cz\r\nX-Requested-With: XMLHttpRequest\r\n\r\n'
    class sock:
        def __init__(self):
            self.family = 'AddressFamily.AF_INET'
            self.type = 'SocketKind.SOCK_STREAM'
            self.proto = 'Protocol-0'
    p = sock()
    f = HTTPRequest(data,p,('94.112.152.4','59196'))
    f.print_data()

