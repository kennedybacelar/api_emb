import requests

def embonor_auth(api_params):

    #We are using as authentication the api_link/product as the endpoint to check if the API is on
    url = f"{api_params['API_URL']}/Product"
    key = api_params['Authorization']

    response = requests.get(url=url, headers={'Authorization': key})

    return response.ok

