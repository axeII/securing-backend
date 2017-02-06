"""This is the sql injection module.

SQL injection attacks allow attackers to spoof identity, tamper with existing data, cause repudiation issues such as voiding transactions or changing balances, allow the complete disclosure of all data on the system, destroy the data or make it otherwise unavailable, and become administrators of the database server.
"""

__all__ = ['match_exploit']
__version__ = '0.3'
__author__ = 'Ales Lerch'

from urllib.parse import urlparse
from re import match
import logging

logger = logging.getLogger('mainLogger')

def match_exploit(data):
    if isinstance(data,dict):
        try:
            if data['Command'] == 'GET':

                data_list = (
                        data['Referer'],data['Path'],data['Cookie'],
                        )
                for dat in data_list:
                    url = urlparse(dat)
                    urlq = url.query
                    urlp = url.path
                    l = [
                            'Mozilla','Chrome','Firefox',
                            'Windows','NT','Gecko',
                            'Safari','Macintosh',
                            ]

                    if match(r'.+?[/\w][0-9]\.[0-9]',urlq) or any(word 
                            in urlq for word in l):
                        return True

                    if data['User-Agent'] in data['Referer'] and data['User-Agent']:
                        return True

                    special_keys = (
                            'OR','AND','UNION',
                            'SELECT','LIMIT','ALL',
                            'DATABASE()','VERSION()','FROM',
                            'USER()','PASSWORD()','TABLE_NAME',
                            'WHERE','EXEC','CONCAT',
                            'GROUP','NULL','ASCII',
                            'SUBSTRING','DUAL','SLEEP',
                            'TRUE','FALSE','LIKE',
                            )
                    if any(sk in urlq or sk.lower() in urlq for sk in special_keys):
                        return True 

                    if match(r"'\s*--(\s|')'\s*(and|or|xor|&&|\|\|)\s*\(?\s*('|[0-9]|`?[a-z\._-]+`?\s*(=|like)|[a-z]+\s*\()'\s*(not\s+)?in\s*\(\s*['0-9]union(\s+all)?(\s*\(\s*|\s+)select(`|\s)select(\s*`|\s+)(\*|[a-z0-9_\, ]*)(`\s*|\s+)from(\s*`|\s+)[a-z0-9_\.]*insert\s+into(\s*`|\s+).*(`\s*|\s+)(values\s*)?\(.*\)update(\s*`|\s+)[a-z0-9_\.]*(`\s*|\s+)set(\s*`|\s+).*=delete\s+from(\s*`|\s+)[a-z0-9_\.]*`?",urlq) or match(r"/\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))/ix",urlq):
                        return True

            if data['Command'] == 'POST':
                #testuj POST metodu
                pass

        except KeyError as k:
            logger.error('Empty input data %s no control with rule' % k,__name__)

    return False


if __name__ == "__main__":
    print(match_exploit({'Command':'GET','Referer':'http://www.example.com/product.php?id=10 AND 1=2','User-Agent':'','Path':'','Cookie':''}))
    print(match_exploit({'Command':'GET','Referer':'http://www.example.com/product.php?Mozilla/5.0 (Windows NT 6.2; rv:15.0) Gecko/20100101 Firefox/15.0','User-Agent':'','Path':'','Cookie':''}))
    print(match_exploit({'Command':'GET','Referer':"http://www.example.com/index.php?username=1'%20or%20'1'%20=%20'1&password=1'%20or%20'1'%20=%20'1",'User-Agent':'','Path':'','Cookie':''}))
    print(match_exploit({'Command':'GET','Referer':"http://www.example.com/product.php?id=10",'User-Agent':'','Path':'','Cookie':''}))

