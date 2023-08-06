import logging
import os
from pathlib import Path
import sys
import datetime
from logging import handlers

LEVEL_LIST = ['NOTSET', 'INFO', 'DEBUG', 'ERROR', 'WARNING', 'CRITICAL']

class DailyRotatingFileHandler(handlers.RotatingFileHandler):

    def __init__(self, basedir, logfilename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0):
        """
        @summary: 
        Set self.baseFilename to date string of today.
        The handler create logFile named self.baseFilename
        """
        self.basedir_ = basedir
        self.logfilename = logfilename
        self.baseFilename = self.getBaseFilename()
        handlers.RotatingFileHandler.__init__(self, self.baseFilename, mode, maxBytes, backupCount, encoding, delay)

    def getBaseFilename(self):
        """
        @summary: Return logFile name string formatted to "today.log.alias"
        """
        self.today_ = datetime.date.today()
        subdir_ = self.basedir_ / datetime.datetime.now().strftime("%Y%m%d")
        subdir_.mkdir(parents=True, exist_ok=True)
        basename_ = self.logfilename
        return os.path.join(subdir_, basename_)

    def shouldRollover(self, record):
        """
        @summary: 
        Rollover happen 
        1. When the logFile size is get over maxBytes.
        2. When date is changed.

        @see: BaseRotatingHandler.emit
        """

        if self.stream is None:                
            self.stream = self._open()

        if self.maxBytes > 0 :                  
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1

        if self.today_ != datetime.date.today():
            self.baseFilename = self.getBaseFilename()
            return 1

        return 0
    
class logger_x(object):
    def __init__(self, file, console=None, rfile=None, maxBytes=0, backupCount=0):
        self.formatter = logging.Formatter('[%(asctime)s] [PID:%(process)d ThreadID:%(thread)d] [%(levelname)s] [%(name)s.%(funcName)s:%(lineno)d]  %(message)s')
        self.name = Path(file).stem
        self.file = Path(file).parent.absolute()
        self.s_console = console if console and console in LEVEL_LIST else 'DEBUG'
        self.r_file = rfile if rfile and rfile in LEVEL_LIST else 'DEBUG'
        self.log_path = self.file / "log"
        self.log_name = self.name + '.log'
        self.full_path = self.log_path / self.log_name
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def namer(self, name):
        return name.replace(".log", "") + ".log"

    def configLogger(self):
        logging.getLogger().setLevel(level=self.s_console)
        logging.getLogger("filelock").setLevel(logging.ERROR) ## Avoid lockfile log
        fileHandler = DailyRotatingFileHandler(self.log_path, self.log_name, maxBytes=self.maxBytes, backupCount=self.backupCount, encoding='utf-8', delay=0)
        logging.getLogger().handlers.clear()
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(level=self.s_console)
        consoleHandler.setFormatter(self.formatter)
        logging.getLogger().addHandler(consoleHandler)
        fileHandler.namer = self.namer
        fileHandler.setLevel(level=self.r_file)
        fileHandler.setFormatter(self.formatter)
        logging.getLogger().addHandler(fileHandler)
        log = logging.getLogger("app." + self.name)
        return log

if __name__ == '__main__':
    loggerX = logger_x(__file__)
    log = loggerX.configLogger()
    log.info('THIS is info msg !!')
    log.debug('THIS is debug msg !!')
    log.error('THIS is error msg !!')
    log.warning('THIS is warning msg !!')
    log.critical('THIS is critical msg !!')
