'''
*****************************
ExergenicsLogger.class.py
*****************************

N.WONG FEB 2023
Implements exergenics internal application logging by providing a Logtail interface
'''

import os
import inspect
import logging
from logtail import LogtailHandler


class Singleton (type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ExergenicsLogger(metaclass=Singleton):
    """Exergenics Logger class to send structured logs directly to https://logtail.com/. 

    The Exergenics Logger is built using the Python Singleton pattern and only needed to be initialised 
    once and the same instance will be reused throughout the module. To start using the Logger, 
    initialise once by providing __init__() arguments and subsequent inovation  
    arguments.

    HOW TO USE EXERGENICSLOGGER

    In main function: 

    from exergenics import exergenics.ExergenicsLogger as Logger
    logger = Logger('loggerName', 'component', 'subcomponent', 'jobId', 'environment')

    In sub-functions:

    logger = Logger()
    logger.info('message')

    """

    def __init__(self, loggerName: str,  component: str = '', subComponent: str = '', jobId: str = '', environment: str = '') -> None:

        # Exergenics Logger version number
        self._version = 1.0

        # Configure logtail API key
        API_KEY = os.getenv('LOGTAIL_API_KEY')
        if not API_KEY:
            raise Exception(
                'LOGTAIL_API_KEY not found in environment variables!')

        # Configure logtail logging
        self._handler = LogtailHandler(source_token=API_KEY)
        self._logger = logging.getLogger(loggerName)
        self._logger.handlers = []
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self._handler)

        # Custom field to allow filtering
        self._extra = {
            'component': component,
            'sub_component': subComponent,
            'job_id': jobId,
            'environment': environment
        }

    def _setFunctionName(self) -> None:
        """ Retrieve function name from stack and add to logtail _extra field."""
        functionName = inspect.stack()[2][3]
        self._extra['function'] = functionName
        return None

    def debug(self, message: str) -> None:
        """Send logs with DEBUG level.

        Parameter
        ---------
        message : str
            Debug log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.debug(message, extra=self._extra)
        return None

    def info(self, message: str) -> None:
        """Send logs with INFO level.

        Parameter
        ---------
        message : str
            Info log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.info(message, extra=self._extra)
        return None

    def warn(self, message: str) -> None:
        """Send logs with WARN level.

        Parameter
        ---------
        message : str
            Warning log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.warn(message, extra=self._extra)
        return None

    def error(self, message: str) -> None:
        """Send logs with ERROR level.

        Parameter
        ---------
        message : str
            Error log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.error(message, extra=self._extra)
        return None

    def getVersion(self) -> str:
        """Get current Exergenic Logger version number.

        Returns
        -------
        str
            Logger version in string
        """
        return str(self._version)
