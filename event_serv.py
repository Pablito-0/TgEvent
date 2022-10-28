import requests


class EventPlaygroundService:
    limit = 1
    base_url = "http://localhost:8000/base/"

    def get_users(self, page=1):
        query_params = dict(limit=self.limit, offset=(int(page) - 1) * self.limit)
        response = requests.get(f"{self.base_url}users", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id: int):
        response = requests.get(f'{self.base_url}users/{user_id}/')
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: int, user_data: dict):
        response = requests.patch(f'{self.base_url}users/{user_id}/', data=user_data)
        response.raise_for_status()
        return response.json()


event_service = EventPlaygroundService()
