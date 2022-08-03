from tkinter import messagebox
import json


class SaveAndLoad:

    """
    This class provides the mechanism to save and load json data locally pertaining to the Pixela Control Panel App
    """

    @staticmethod
    def get_userdata():

        """
        Get user_data from data.json file
                Return: user_data (json): Returns user data from data.json file, which includes username,
                                          token and graph_id data
        """

        user_data = None
        try:
            with open(file="data.json", mode="r") as data_file:
                user_data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No Data File Found")
        finally:
            return user_data

    @staticmethod
    def save(username, graph_list=None, token=None):

        """
        Saves username, graph_id and token to data.json file

            Parameters:
                    username (str): Username to be saved locally to mirror username registered with Pixela API
                    graph_list (str): Graph ID to be saved locally to mirror graph ID registered with Pixela API
                    token (str): Token password to be saved locally to mirror token used for registering new user with
                                 Pixela API
        """

        if graph_list is None:
            graph_list = []
        new_data = {
            username: {
                "token": token,
                "graph_id": graph_list
            }
        }

        try:
            with open(file="data.json", mode="r") as data_file:
                # Read old data
                userdata = json.load(data_file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            if username in userdata:

                userdata[username]["graph_id"] = graph_list

            else:
                # Update old data with new data
                userdata.update(new_data)

            with open(file="data.json", mode="w") as data_file:
                json.dump(userdata, data_file, indent=4)

