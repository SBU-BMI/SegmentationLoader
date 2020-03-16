import requests


class MyApi:
    host = None
    username = None
    password = None
    cookie = None

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        try:
            self.cookie = self.get_cookie()
            if self.cookie is None:
                raise Exception("Request for cookie failed.")
        except Exception as e:
            print("Exception: {}".format(e))

    def get_cookie(self):
        try:
            auth = "{\"name\":\"" + self.username + "\", \"pass\": \"" + self.password + "\"}"
            r1 = requests.post(self.host + '/user/login?_format=json', data=auth)
        except Exception as e:
            print("Exception: {}".format(e))
            return None
        else:
            return r1.cookies

    def get_data(self, url):
        # make our API request
        r2 = requests.get(self.host + url, cookies=self.cookie)
        if 'json' in r2.headers.get('Content-Type'):
            js = r2.json()
        else:
            print("Didn't get json. Response headers: {}".format(r2.headers))
            js = None

        return js

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

    def get_collection_lookup_table(self):
        response = self.get_data('/collections?_format=json')
        lookup_table = {}

        if len(response) > 0:
            for r in response:
                collection_name = r['name'][0]['value']
                collection_id = r['tid'][0]['value']
                lookup_table[collection_id] = collection_name

        return lookup_table

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
