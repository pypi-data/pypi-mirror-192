import requests
import json


class SuccessFactorsApi:
    """
    SuccessFactors API connector
    """

    def __init__(self, host, user, password, endpoint, parameters):
        self.host = host
        self.user = user
        self.password = password
        self.endpoint = endpoint
        self.parameters = parameters

    def __has_more_data(self, data):
        """
        Checks if there are more data to retrieve
        """
        return True if "d" in data and "__next" in data["d"] else False

    def __get_next_endpoint(self, data):
        """
        Gets the endpoint for retrieving more data
        """
        return data["d"]["__next"]

    def __parse_records(self, records):
        """
        Parses the records collection
        """
        if "d" not in records:
            raise Exception(
                "The SFSF query service has returned corrupted data.")
        if "results" not in records["d"]:
            raise Exception(
                "The SFSF query service has returned corrupted data.")

        return records["d"]["results"]

    def __send_request(self, endpoint):
        """
        Gets data from SuccessFactors
        """
        response = requests.get(endpoint, auth=(self.user, self.password))

        return response if response.status_code == 200 else False

    def get_data(self):
        """
        Retrieves the queried data
        """
        endpoint = self.host + self.endpoint + self.parameters
        has_more_data = True
        records = []

        while has_more_data:
            response = self.__send_request(endpoint)
            if not response:
                break
            data = json.loads(response.content)
            records = records + self.__parse_records(data)
            has_more_data = self.__has_more_data(data)
            if has_more_data:
                endpoint = self.__get_next_endpoint(data)

        if not response:
            raise Exception("The SFSF query service has failed")
        else:
            return records
