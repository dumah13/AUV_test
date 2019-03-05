"""
Module includes BaseSensor class
"""
from threading import Thread
from LogPy.LogPy import Logger


class BaseController():
    """
    All controllers in sensors directory shoud inherit from this class
    """
    def __init__(self, main_logger=None, local_log=False, log_directory=""):
        """
        :param main_logger: reference to external logger
        :param local_log: create local file with logs
        :param log_directory: directory for file with local logs
        """
        self.main_logger = main_logger
        self.local_logger = None
        if local_log:
            self.local_logger = Logger(filename=self.__class__.__name__.lower(),
                                       log_directory=log_directory,
                                       title=self.__class__.__name__)
            self.local_logger_thread = Thread(target=self.local_logger,
                                              name='My Logger')
            self.local_logger_thread.start()

    def run(self):
        """
        This method is called by main thread to start
        all additional threads for sensor's object
        If class does not need separate thread,
        implement this method with pass

        In case of sensor logging - place for start logging thread
        """
        pass

    def close(self):
        """
        This method is called by main thread to close
        all additional threads for sensor's object
        and related activities
        If class does not need to close separate thread,
        implement this method with pass
        """
        pass

    def log(self, msg, logtype=''):
        """
        Send log to main and local logger
        
        :param msg: string which contain message for log
        :param logtype: message logtype, log type; available:
            'info', 'warning', 'error', 'fatal'
        """
        if self.main_logger:
            self.main_logger.log(msg, logtype)

        if self.local_logger:
            self.local_logger.log(msg, logtype)
