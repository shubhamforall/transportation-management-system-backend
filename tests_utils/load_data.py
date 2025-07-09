from auth_user.db_access import (
    user_manager,
)


class LoadDataFromInlineData:
    def load_user_data(self):
        user_data = {
            "user_id": "ed0b2cfb-864a-4c34-93d1-8876bbb5cd7a",
            "email": "test.user@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "9878786565",
            "password": "TestUser@123",
        }
        return user_manager.create(data=user_data)

    def delete_all_records(self):
        user_manager.delete(soft_delete=False, force_delete=True)


def load_test_data():
    loader = LoadDataFromInlineData()
    loader.delete_all_records()
    loader.load_user_data()
