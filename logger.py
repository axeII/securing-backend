"""This is Logger model

Makes that everythign is loged to standart output or into specific log file.
"""
__author__ = "Ales Lerch"

import os
import logging
import datetime

FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
DATE = "%m/%d/%Y %H:%M:%S"
LOGS = "./logs"

def createLogger(name="default_log",strm=False):

    def setFileHandler(format_ = FORMAT,datef = DATE):
        date_ = datetime.datetime.now().strftime("[%Y-%m-%d][%H:%M:%S]")
        file_name = "{}/{}.log".format(LOGS,date_)
        formatter = logging.Formatter(format_,datef)
        try:
            filehandler = logging.FileHandler(file_name,"w")
        except FileNotFoundError as fl:
            print('[Error] Folder for logging not found!\n[Info] Creating new'
            ' folder...\n[Info] Folder created! Logging now...')
            os.mkdir(LOGS)
            filehandler = logging.FileHandler(file_name,"w")
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        return filehandler

    def setStreamHandler():
        formatter = logging.Formatter(FORMAT,DATE)
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.DEBUG)
        streamhandler.setFormatter(formatter)
        return streamhandler

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if strm:
        logger.addHandler(setStreamHandler())
    else:
        logger.addHandler(setFileHandler())

    return logger
