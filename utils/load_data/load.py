import json
from auth_user.db_access import user_manager
from auth_user.models import User


class LoadDataFromFiles:
    def load_user_data(self):
        data = self.read_file("user")
        user_data = data.get("data")
        return user_manager.create(data=user_data, many=True)

    def delete_all_records(self):
        User.objects.all().delete()

    def read_file(self, file_path):
        with open(f"utils/load_data/json_data/{file_path}.json", "r") as conf_file:
            return json.load(conf_file)


def load_data():
    loader = LoadDataFromFiles()
    loader.delete_all_records()
    loader.load_user_data()
