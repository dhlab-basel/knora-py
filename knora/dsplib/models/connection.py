import requests
import json
from pystrict import strict
from typing import List, Set, Dict, Tuple, Optional, Any, Union

from .helpers import Actions, BaseError


@strict
class Connection:
    """
    An Connection instance represents a connection to a Knora server.

    Attributes
    ----------

    none (internal use attributes should not be modified/set directly)
    """

    server: str
    prefixes: Union[Dict[str, str], None]
    token: Union[str, None]

    def __init__(self, server: str, prefixes: Dict[str, str] = None):
        """
        Constructor requiring the server address, the user and password of KNORA
        :param server: Address of the server, e.g https://api.dasch.swiss
        :param prefixes: Ontology prefixes used
        """

        self.server = server
        self.prefixes = prefixes
        self.token = None

    def login(self, email: str, password: str) -> None:
        """
        Method to login into KNORA which creates a session token.
        :param email: Email of user, e.g., root@example.com
        :param password: Password of the user, e.g. test
        """

        credentials = {
            "email": email,
            "password": password
        }
        jsondata = json.dumps(credentials)

        req = requests.post(
            self.server + '/v2/authentication',
            headers={'Content-Type': 'application/json; charset=UTF-8'},
            data=jsondata
        )
        self.on_api_error(req)
        result = req.json()
        self.token = result["token"]

    def get_token(self) -> str:
        """
        Returns the token
        :return: token string
        """

        return self.token

    def logout(self) -> None:
        """
        Performs a logout
        :return: None
        """

        if self.token is not None:
            req = requests.delete(
                self.server + '/v2/authentication',
                headers={'Authorization': 'Bearer ' + self.token}
            )
            self.on_api_error(req)
            self.token = None

    def __del__(self):
        pass
        #self.logout()

    def on_api_error(self, res) -> None:
        """
        Method to check for any API errors
        :param res: The input to check, usually JSON format
        :return: Possible Error that is being raised
        """

        if res.status_code != 200:
            raise BaseError("KNORA-ERROR: status code=" + str(res.status_code) + "\nMessage:" + res.text)

        if 'error' in res:
            raise BaseError("KNORA-ERROR: API error: " + res.error)

    def post(self, path: str, jsondata: Optional[str] = None):
        """
        Post Json data to a given server using a HTTP POST request
        :param path: Path of RESTful route
        :param jsondata: Valid JSON as string
        :return: Response from server
        """

        if path[0] != '/':
            path = '/' + path
        if jsondata is None:
            if self.token is not None:
                req = requests.post(self.server + path,
                                    headers={'Authorization': 'Bearer ' + self.token})
            else:
                req = requests.post(self.server + path)
        else:
            if self.token is not None:
                req = requests.post(self.server + path,
                                    headers={'Content-Type': 'application/json; charset=UTF-8',
                                             'Authorization': 'Bearer ' + self.token},
                                    data=jsondata)
            else:
                req = requests.post(self.server + path,
                                    headers={'Content-Type': 'application/json; charset=UTF-8'},
                                    data=jsondata)
        self.on_api_error(req)
        result = req.json()
        return result

    def get(self, path: str, headers: Optional[Dict[str, str]] = None):
        """
        Get data from a server using a HTTP GET request
        :param path: Path of RESTful route
        :param headers: ...
        :return: Response from server
        """

        if path[0] != '/':
            path = '/' + path
        if self.token is None:
            if headers is None:
                req = requests.get(self.server + path)
            else:
                req = requests.get(self.server + path, headers)
        else:
            if headers is None:
                req = requests.get(self.server + path,
                                   headers={'Authorization': 'Bearer ' + self.token})
            else:
                headers['Authorization'] = 'Bearer ' + self.token
                req = requests.get(self.server + path, headers)

        self.on_api_error(req)
        result = req.json()
        return result

    def put(self, path: str, jsondata: Optional[str] = None, content_type: str = 'application/json'):
        """
        Send data to a RESTful server using a HTTP PUT request
        :param path: Path of RESTful route
        :param jsondata: Valid JSON as string
        :param content_type: HTTP Content-Type [default: 'application/json']
        :return:
        """

        if path[0] != '/':
            path = '/' + path
        if jsondata is None:
            req = requests.put(self.server + path,
                               headers={'Authorization': 'Bearer ' + self.token})
        else:
            req = requests.put(self.server + path,
                               headers={'Content-Type': content_type + '; charset=UTF-8',
                                        'Authorization': 'Bearer ' + self.token},
                               data=jsondata)
        self.on_api_error(req)
        result = req.json()
        return result

    def delete(self, path: str, params: Optional[any] = None):
        """
        Send a delete request using the HTTP DELETE request
        :param path: Path of RESTful route
        :return: Response from server
        """

        if path[0] != '/':
            path = '/' + path
        if params is not None:
            req = requests.delete(self.server + path,
                                  headers={'Authorization': 'Bearer ' + self.token},
                                  params=params)

        else:
            req = requests.delete(self.server + path,
                                  headers={'Authorization': 'Bearer ' + self.token})
        self.on_api_error(req)
        result = req.json()
        return result

    def reset_triplestore_content(self):
        rdfdata = [
            {
                "path": "./knora-ontologies/knora-admin.ttl",
                "name": "http://www.knora.org/ontology/knora-admin"
            },
            {
                "path": "./knora-ontologies/knora-base.ttl",
                "name": "http://www.knora.org/ontology/knora-base"
            },
            {
                "path": "./knora-ontologies/standoff-onto.ttl",
                "name": "http://www.knora.org/ontology/standoff"
            },
            {
                "path": "./knora-ontologies/standoff-data.ttl",
                "name": "http://www.knora.org/data/standoff"
            },
            {
                "path": "./knora-ontologies/salsah-gui.ttl",
                "name": "http://www.knora.org/ontology/salsah-gui"
            },
            {
                "path": "./_test_data/all_data/admin-data.ttl",
                "name": "http://www.knora.org/data/admin"
            },
            {
                "path": "./_test_data/all_data/permissions-data.ttl",
                "name": "http://www.knora.org/data/permissions"
            },
            {
                "path": "./_test_data/all_data/system-data.ttl",
                "name": "http://www.knora.org/data/0000/SystemProject"
            }
        ]
        jsondata = json.dumps(rdfdata)
        url = self.server + '/admin/store/ResetTriplestoreContent?prependdefaults=false'

        req = requests.post(url,
                            headers={'Content-Type': 'application/json; charset=UTF-8'},
                            data=jsondata)
        self.on_api_error(req)
        res = req.json()
        #  pprint(res)
        return res


