"""User API client."""
from api.client import APIClient
from models.user import UserData, UserResponse


class UserAPI(APIClient):
    """User operations."""

    def create_user(self, user_data: UserData):
        """Create new user."""
        data = {"user": user_data.to_dict()}
        resp = self.post("/users", data=data)

        if resp.status_code == 200:
            json_data = resp.json()
            if "User-Token" in json_data:
                self.set_user_token(json_data["User-Token"])

        return resp

    def get_user(self, login: str, authenticated=False):
        """Get user info."""
        return self.get(f"/users/{login}", authenticated=authenticated)

    def get_user_model(self, login: str, authenticated=False) -> UserResponse:
        """Get user as model."""
        resp = self.get_user(login, authenticated)
        return UserResponse.from_dict(resp.json())

    def update_user(self, current_login: str, **kwargs):
        """Update user fields."""
        data = {"user": kwargs}
        return self.put(f"/users/{current_login}", data=data, authenticated=True)

    def create_session(self, login: str, password: str):
        """Login."""
        data = {"user": {"login": login, "password": password}}
        resp = self.post("/session", data=data)

        if resp.status_code == 200:
            json_data = resp.json()
            if "User-Token" in json_data:
                self.set_user_token(json_data["User-Token"])

        return resp

    def destroy_session(self):
        """Logout."""
        return self.delete("/session", authenticated=True)
