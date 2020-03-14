import time
import requests


class MyApi:
    host = None
    username = None
    password = None
    access_token = None
    access_token_expiration = None

    def __init__(self, host, username, password):
        # the function that is executed when
        # an instance of the class is created
        self.host = host
        self.username = username
        self.password = password

        try:
            self.access_token = self.get_access_token()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            print(e)

    def get_access_token(self):
        # the function that is
        # used to request the JWT
        try:
            # request an access token
            response = requests.get(self.host + "/jwt/token", auth=(self.username, self.password))
            # optional: raise exception for status code
            response.raise_for_status()
        except Exception as e:
            print(e)
            return None
        else:
            self.access_token_expiration = time.time() + 3500
            # assuming the response's structure is
            # {"token": ""}
            return response.json()['token']

    class Decorators:
        @staticmethod
        def refresh_token(decorated):
            # the function that is used to check
            # the JWT and refresh if necessary
            def wrapper(api, *args, **kwargs):
                print("api token expire: {}".format(api.access_token_expiration))
                print("time: {}".format(time.time()))
                print("Expires in: {}".format(api.access_token_expiration - time.time()))
                if api.access_token_expiration - time.time() <= 0:
                    print("WE'RE HERE!")
                    api.get_access_token()
                return decorated(api, *args, **kwargs)

            return wrapper

    @Decorators.refresh_token
    def get_data(self, url):
        # make our API request
        r = requests.get(self.host + url, headers={"Authorization": "Bearer " + self.access_token})
        if 'json' in r.headers.get('Content-Type'):
            js = r.json()
        else:
            print("Response content is not in JSON format: {}".format(r))
            js = None
        return js

    @Decorators.refresh_token
    def get_collection_info(self, collection):
        collection_id = 0
        collection_name = ""
        a_dict = self.get_collection_lookup_table()

        if len(a_dict) > 0:
            for key in a_dict:
                if str(a_dict[key]).lower() in collection.lower():
                    collection_name = a_dict[key]
                    collection_id = key
                    break

        return collection_id, collection_name

    @Decorators.refresh_token
    def get_collection_lookup_table(self):
        response = self.get_data('/collections?_format=json')
        lookup_table = {}

        if len(response) > 0:
            for r in response:
                collection_name = r['name'][0]['value']
                collection_id = r['tid'][0]['value']
                lookup_table[collection_id] = collection_name

        return lookup_table

    @Decorators.refresh_token
    def get_featuremaps(self, slide_id):
        """
        Returns list of Featuremap Execution IDs
        """
        my_set = set()

        response = self.get_data('/maps/' + str(slide_id) + '?_format=json')

        if len(response) > 0:
            for r in response:
                exec = r['execution_id']
                if len(exec) > 0:
                    my_set.add(exec[0]['value'])
                else:
                    map_type = r['field_map_type']
                    if len(map_type) > 0:
                        my_set.add(map_type[0]['value'])

        return my_set
