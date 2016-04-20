
import logging


logger_inited = None


def logger(name):
    if not logger_inited:
        logging.basicConfig(
                format='%(asctime)s %(levelname)s[%(module)s:%(lineno)d]: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='../app.log',
                level=logging.DEBUG)
        logging.debug('logger initialized')

    return logging.getLogger(name)
