"""Main of application

This is main which activates whole application
"""
__author__ = 'Ales Lerch'

import logger
import server_side

PRINTOUT = True
GENDATA = False

def runApplication():
    pass

if __name__ == "__main__":

    main_logger = logger.createLogger('mainLogger',PRINTOUT)

    try:
        main_logger.debug('Starting application YAY!')
        ss = server_side.ServerSide('localhost',8887,GENDATA)
        ss.activate_mock_server()
    except KeyboardInterrupt:
        ss.shut_down()
        main_logger.debug('Ending application COME BACK SOON!')

