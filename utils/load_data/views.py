import json

from rest_framework.views import APIView

from utils.response import generate_response
from auth_user.db_access import (
    user_manager,
)
from auth_user.models import User


class LoadPreDataView(APIView):
    __doc__ = """
        This is the view for loading pre-defined data into the database.
        It reads data from JSON files and populates the database with it.
    """

    def get(self, request):
        """dump data in databases reading json file and django models"""

        load_data_obj = LoadDataFromFiles()
        load_data_obj.delete_all_records()
        load_data_obj.load_user_data() 

        return generate_response(data={"success": "Data dumped successfully"})


class LoadDataFromFiles:

    def load_user_data(self):
        data = self.read_file("user")
        print("Data loaded from file:", data)
        user_data = data.get("data")
        return user_manager.create(data=user_data, many=True)

    def delete_all_records(self):
        """
        Deletes all the records of  User models
        """
        User.objects.all().delete()


    def read_file(self, file_path):
        with open(f"utils/load_data/json_data/{file_path}.json", "r") as conf_file:
            return json.load(conf_file)
