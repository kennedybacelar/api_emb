import os, requests, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import time

from CONTROL.embonor_file_io import load_config
from AUTH.embonor_auth import embonor_auth

def general_retry(func):
    max_retry = 3
    def wrap(*args, **kwargs):
        for _ in range(max_retry):
            try:
                print(f'Tentativa: {_}\n')
                return func(*args, **kwargs)
            except Exception as error:
                time.sleep(1)
                err = error
        raise err
    return wrap

class EmbonorAPI():

    def __init__(self):

        info_config_filename = 'CONFIG/info.cfg'

        self.api_params = load_config(info_config_filename)
        self.url = self.api_params['API_URL']

        if not embonor_auth(self.api_params):
            raise Exception('Authentication failed')

    @general_retry
    def call_api(self, call_string):

        endpoint = f'{self.url}/{call_string}'
        response = requests.get(url=endpoint, headers=self.api_params)

        return response.json()
