import os
from configparser import RawConfigParser, NoOptionError, NoSectionError


def read_config_file(key, param):
    config = RawConfigParser()
    config.read(os.environ["BIZ_AUTOMATION_ENV"])
    result = config.get(key, param)
    return result

def set_config_file(key, param, value):
    config = RawConfigParser()
    config.read(os.environ["BIZ_AUTOMATION_ENV"])
    config.set(key, param, value)
    cfgfile = open(os.environ["BIZ_AUTOMATION_ENV"], 'w')
    config.write(cfgfile, space_around_delimiters=True)
    cfgfile.close()
    return config.get(key, param)

def get_values_of_section(environ_var, section):
    config = RawConfigParser()
    values = []

    try:
        config.read(os.environ[environ_var])
        result = config.options(section)
    except NoSectionError:
        config.read(os.environ["LOCAL_CONFIG"])
        result = config.options(section)

    for option in result:
        value = config.get(section, option)
        values.append(value)
    return values
