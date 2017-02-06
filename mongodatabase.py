"""This is mongodb database module

This modules saves exploits to NoSQL mongodb database as dict format.
"""

#from __future__ import print_function

__author__ = 'Ales Lerch'

from pymongo import MongoClient
import logging
import uuid

class ExploitMDB:
    DATABASE = 'exploitsdbs'
    COLLECTION = 'exploits'

    def __init__(self,host = 'localhost',port = 27017):
        self.myClient = MongoClient(host,port)
        self.myDB = self.myClient[self.DATABASE]
        self.myCollection = self.myDB[self.COLLECTION]
        self.log = logging.getLogger('mainLogger')

    def save(self,expl):
        if expl and isinstance(expl,dict):

            key = uuid.uuid1().hex
            sec_key = str(uuid.uuid4().int)[:-1]
            second_key = self._generate_key(expl)
            if key and second_key:
                expl['_id'] = key
                expl['second_id'] = sec_key
                expl['total_exploit'] = 1

                try:
                    self.myDB.exploits.insert(expl)
                    return True
                except Exception as e:
                    self.log.error('Cannot insert new document into collectinon,%s'
                            % e)
            else:
                self.log.error('Primary key or secondary key is empty. Cannot '
                        'save data.')
        return False

    def get_all(self):
        return self.myDB.myCollection.find()

    def get_specific(self,keys):
        if keys and isinstance(keys,dict) and len(keys) > 0:
            return self.myDB.exploits.find(projection=keys)


    def _generate_key(self, exp):
        try:
            return exp['attacktype'] + '_' + exp['time'].replace('-','/')[:10]
        except KeyError as k:
            self.log.error('Cannot generate key - missing key: %s' % k)
            return ''

if __name__ == "__main__":
    exdb = ExploitMDB()
    exdb.save({"Host" : [ "localhost:8887" ], "Command" : [ "GET" ], "Version": [ "HTTP/1.1" ],
        "Time" : [ "2016-09-23 11:32:57" ], "second_id" : "r_2016-09-23 11:32:57",
        "User_Agent" : [ "Mozilla/5.0 (Macintosh;Intel Mac OS X 10_11_6)"
        " AppleWebKit/602.1.50 (KHTML, like Gecko)Version/10.0 Safari/602.1.50" ],
        "Socket_info" : [
            "AddressFamily.AF_INET,SocketKind.SOCK_STREAM,Protocol 0" ],
        "Accept_Language" : [ "cs-cz" ], "Upgrade_Insecure_Requests" : [ "1" ],
        "Path" : [ "/" ], "Error" : [ 'null' ], "Client_address" : [ "IPAddress:127.0.0.1,port:65156" ],
        "Accept" : [
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            ], "Cookie" : [ "SQLiteManager_currentLangue=2" ], "Connection" : ["keep-alive" ],
        "AttackType" : "rules.url_misiterprt","Accept_Encoding" : [ "gzip,deflate" ] })
