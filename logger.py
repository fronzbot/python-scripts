import logging
import logging.handlers

LOGGER = logging.getLogger('pycron')
LOGGER.setLevel(logging.DEBUG)

HANDLER = logging.handlers.SysLogHandler('/dev/log')
FORMATTER = logging.Formatter('%(levelname)s [%(module)s.%(funcName)s]: %(message)s')
HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER)
