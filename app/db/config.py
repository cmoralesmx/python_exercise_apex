import logging
from configparser import ConfigParser

# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


def config(filename:str ='/app/secrets/config.ini', section:str = 'postgres') -> dict:
    """Load the configuration parameters from config.ini"""
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(
            section,
            filename))
    logging.debug('config.ini loaded')
    return db
