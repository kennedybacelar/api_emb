"""

    Function responsible for reading the input parameters of info.cfg file

"""

def load_config(_filename=''):
    return {_key: _value for _key, _value in (l.replace('\n', '').split('=') for  l in open(_filename))}

