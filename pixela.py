import requests
import datetime

pixela_endpoint = "https://pixe.la/v1/users"


class Pixela:

    """
    This class contains all the methods to API endpoint translations required for the GUI to interact with the
    Pixela API

        Attributes:
                username (str): Username registered with Pixela API
                token (str): Token registered with Pixela API
                graph_id_list (str) : List of "Graph_ID" registered with Pixela API
    """

    def __init__(self, username, token, graph_id_list=None):
        if graph_id_list is None:
            graph_id_list = []
        self.username = username
        self.token = token
        self.graph_id = graph_id_list
        self.headers = {
            "X-USER-TOKEN": self.token
        }

    def get_graph_id_list(self):

        """
        Returns a list of "Graph IDs" associated with current Pixela object.
            Return:
                self.graph_id (list) : Returns a list of graph ids associated with current pixela object.
        """

        return self.graph_id

    def update_graph_id_list(self, graph_to_add):

        """
        Appends Pixela object with new "Graph ID" data.
            Parameter:
                    graph_to_add (str) : Takes "Graph ID" of newly registered Pixela graph to add to associated
                                         Pixela object.
        """

        self.graph_id.append(graph_to_add)

    def delete_graph_id(self, graph_to_remove):

        """""
        Deletes selected "Graph ID" data associated with current Pixela object.
                Parameter:
                        graph_to_remove (str) : Takes "Graph ID" successfully deleted from Pixela API to be removed
                                                from associated Pixela object.
        """

        self.graph_id.remove(graph_to_remove)

    def create_user(self):

        """
        Registers a new Pixela user with Pixela API
                Returns:
                        response.json() (json): Returns json formatted response from Pixela API which includes a
                                                string "message" key and a boolean "isSuccess" key.
        """

        user_params = {
            "token": self.token,
            "username": self.username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }

        response = requests.post(url=pixela_endpoint, json=user_params)

        print(response.text)

        return response.json()

    def create_graph(self, graph_id, graph_name, units, unit_type, color):

        """
        Registers a new graph to associated user with Pixela API
                Parameters:
                        graph_id (str): Takes "Graph ID" which identifies graph locally and with Pixela API.
                        graph_name (str) : Takes name of graph to be registered with Pixela API
                        units (str): Takes name of unit associated with graph.
                        unit_type (str): Takes unit type which can be either "integer" or "float".
                        color (str): Takes color which can be "shibafu", "momiji", "sora", "ichou", "ajisai" or "kuro".
                Returns:
                        response.json() (json): Returns json formatted response from Pixela API which includes a
                                                string "message" key and a boolean "isSuccess" key.
        """

        graph_params = {
            "id": graph_id,
            "name": graph_name,
            "unit": units,
            "type": unit_type,
            "color": color
        }

        graph_endpoint = f"{pixela_endpoint}/{self.username}/graphs"
        response = requests.post(url=graph_endpoint, json=graph_params, headers=self.headers)
        print(graph_endpoint)
        print(response.text)

        return response.json()

    def create_pixel(self, quantity, graph_name):

        """
        Register new pixel on graph associated with current Pixela object.
                Parameter:
                        quantity (str): Takes amount value to be represented by a pixel on graph.
                        graph_name (str): Takes nome of graph to add pixel.
                Returns:
                        response.json() (json): Returns json formatted response from Pixela API which includes a
                                                string "message" key and a boolean "isSuccess" key.
        """

        date = datetime.date.today()
        formatted_date = str(date.strftime("%Y%m%d"))

        pixel_creation_params = {
            "date": formatted_date,
            "quantity": quantity
        }

        pixel_creation_endpoint = f"{pixela_endpoint}/{self.username}/graphs/{graph_name}"
        response = requests.post(url=pixel_creation_endpoint, json=pixel_creation_params, headers=self.headers)
        print(pixel_creation_endpoint)
        print(response.text)

        return response.json()

    def delete_graph(self, graph_id):

        """
        Delete graph registered with Pixela API and associated with current Pixela object.
                    Parameter:
                            graph_id (str): Takes "Graph ID" of graph successfully deleted from Pixela API
                    Returns:
                            response.json() (json): Returns json formatted response from Pixela API which includes a
                                                    string "message" key and a boolean "isSuccess" key.
        """

        pixel_delete_endpoint = f"{pixela_endpoint}/{self.username}/graphs/{graph_id}"
        response = requests.delete(url=pixel_delete_endpoint, headers=self.headers)
        print(pixel_delete_endpoint)
        print(response.text)

        return response.json()

