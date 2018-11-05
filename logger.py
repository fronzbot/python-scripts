import logging
import logging.handlers

LOGGER = logging.getLogger('pycron')
LOGGER.setLevel(logging.DEBUG)

HANDLER = logging.handlers.SysLogHandler('/dev/log')
FORMATTER = logging.Formatter('%(module)s.%(funcName)s: %(levelName)s %(message)s')
HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER)
