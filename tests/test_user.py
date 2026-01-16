"""User API tests."""
import uuid

import allure
import pytest

from api.error_codes import ErrorCode, Msg
from api.user_api import UserAPI
from models.user import UserData, UserResponse


@allure.epic("FavQs API")
@allure.feature("User Management")
class TestUserCreation:
    """User creation tests."""

    @allure.story("Registration")
    @allure.title("Create user and verify")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_and_verify(self, api_client, user_data, check):
        """Create user, get info, verify login and email."""
        with allure.step("Create user"):
            resp = api_client.create_user(user_data)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_contains_key(data, "User-Token")
        check.assert_equal(data.get("login"), user_data.login, "login")

        with allure.step("Get user info"):
            resp = api_client.get_user(user_data.login, authenticated=True)
            check.assert_status_code(resp, 200)

        user = UserResponse.from_dict(resp.json())
        check.assert_equal(user.login, user_data.login, "login")
        check.assert_equal(user.email, user_data.email, "email")


@allure.epic("FavQs API")
@allure.feature("User Management")
class TestUserCreationNegative:
    """Negative user creation tests."""

    @allure.story("Registration")
    @allure.title("Create with existing session (error 31)")
    @pytest.mark.regression
    def test_create_with_session(self, created_user, check):
        """Should fail when already logged in."""
        client, _ = created_user
        new_user = UserData.generate(prefix="newuser")

        resp = client.post("/users", data={"user": new_user.to_dict()}, authenticated=True)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_error_code(data, ErrorCode.SESSION_EXISTS)
        check.assert_error_message_contains(data, Msg.SESSION)

    @allure.story("Registration")
    @allure.title("Invalid email")
    @pytest.mark.regression
    def test_invalid_email(self, api_client, check):
        user = UserData(login="test_inv", email="bad-email", password="Test123")

        resp = api_client.create_user(user)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_validation_error(data, "email")
        check.assert_error_message_contains(data, Msg.EMAIL_INVALID)

    @allure.story("Registration")
    @allure.title("Short password")
    @pytest.mark.regression
    def test_short_password(self, api_client, check):
        user = UserData(login="test_short", email="short@test.com", password="1234")

        resp = api_client.create_user(user)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_validation_error(data, "password")
        check.assert_error_message_contains(data, Msg.PWD_SHORT)

    @allure.story("Registration")
    @allure.title("Special chars in login")
    @pytest.mark.regression
    def test_special_chars_login(self, api_client, check):
        user = UserData(login="test@#$", email="spec@test.com", password="Test123")

        resp = api_client.create_user(user)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_error_code(data, ErrorCode.VALIDATION_ERROR)
        check.assert_error_message_contains(data, Msg.LOGIN_CHARS)

    @allure.story("Registration")
    @allure.title("Login too long")
    @pytest.mark.regression
    def test_login_too_long(self, api_client, check):
        user = UserData(login="a" * 21, email="long@test.com", password="Test123")

        resp = api_client.create_user(user)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_error_code(data, ErrorCode.VALIDATION_ERROR)
        check.assert_error_message_contains(data, Msg.LOGIN_LONG)

    @allure.story("Registration")
    @allure.title("Duplicate login")
    @pytest.mark.regression
    def test_duplicate_login(self, created_user, check):
        """Should fail when login already taken."""
        _, existing = created_user

        dup = UserData(
            login=existing.login,
            email=f"dup_{existing.email}",
            password="Test123"
        )

        new_client = UserAPI()
        resp = new_client.create_user(dup)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_error_code(data, ErrorCode.VALIDATION_ERROR)
        check.assert_error_message_contains(data, Msg.LOGIN_CHARS)
        check.assert_error_message_contains(data, Msg.LOGIN_TAKEN)


@allure.epic("FavQs API")
@allure.feature("User Management")
class TestUserCreationBoundary:
    """Boundary tests."""

    @allure.story("Registration")
    @allure.title("Min login length (1 char)")
    @pytest.mark.regression
    def test_min_login(self, api_client, check):
        char = uuid.uuid4().hex[0]
        user = UserData(login=char, email=f"min_{char}@test.com", password="Test123")

        resp = api_client.create_user(user)

        check.assert_status_code(resp, 200)
        data = resp.json()
        if "User-Token" in data:
            check.assert_equal(data.get("login"), user.login, "login")

    @allure.story("Registration")
    @allure.title("Max login length (20 chars)")
    @pytest.mark.regression
    def test_max_login(self, api_client, check):
        uid = uuid.uuid4().hex[:12]
        login = f"max_{uid}"[:20].ljust(20, 'x')
        user = UserData(login=login, email=f"max_{uid}@test.com", password="Test123")

        resp = api_client.create_user(user)

        check.assert_status_code(resp, 200)
        data = resp.json()
        if "User-Token" in data:
            check.assert_equal(data.get("login"), user.login, "login")

    @allure.story("Registration")
    @allure.title("Min password (5 chars)")
    @pytest.mark.regression
    def test_min_password(self, api_client, check):
        user = UserData.generate(prefix="minpwd")
        user.password = "12345"

        resp = api_client.create_user(user)

        check.assert_status_code(resp, 200)
        data = resp.json()
        if "User-Token" in data:
            check.assert_equal(data.get("login"), user.login, "login")


@allure.epic("FavQs API")
@allure.feature("User Management")
class TestUserUpdate:
    """User update tests."""

    @allure.story("Profile Update")
    @allure.title("Update login and email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_update_login_email(self, created_user, updated_user_data, check):
        """Update login/email and verify changes."""
        client, original = created_user

        resp = client.update_user(
            original.login,
            login=updated_user_data.login,
            email=updated_user_data.email
        )
        check.assert_status_code(resp, 200)

        resp = client.get_user(updated_user_data.login, authenticated=True)
        check.assert_status_code(resp, 200)

        user = UserResponse.from_dict(resp.json())
        check.assert_equal(user.login, updated_user_data.login, "login")
        check.assert_equal(user.email, updated_user_data.email, "email")

    @allure.story("Profile Update")
    @allure.title("Update email only")
    @pytest.mark.regression
    def test_update_email_only(self, created_user, unique_email, check):
        client, original = created_user

        resp = client.update_user(original.login, email=unique_email)
        check.assert_status_code(resp, 200)

        resp = client.get_user(original.login, authenticated=True)
        user = UserResponse.from_dict(resp.json())
        check.assert_equal(user.login, original.login, "login")
        check.assert_equal(user.email, unique_email, "email")

    @allure.story("Profile Update")
    @allure.title("Clear pic")
    @pytest.mark.regression
    def test_clear_pic(self, api_client, user_data, check):
        resp = api_client.create_user(user_data)
        check.assert_status_code(resp, 200)

        resp = api_client.update_user(user_data.login, pic="")

        check.assert_status_code(resp, 200)
        check.assert_success_message(resp.json())

    @allure.story("Profile Update")
    @allure.title("Toggle profanity filter")
    @pytest.mark.regression
    @pytest.mark.parametrize("value", [True, False])
    def test_profanity_filter(self, api_client, user_data, check, value):
        resp = api_client.create_user(user_data)
        check.assert_status_code(resp, 200)

        resp = api_client.update_user(user_data.login, profanity_filter=value)

        check.assert_status_code(resp, 200)
        check.assert_success_message(resp.json())

    @allure.story("Profile Update")
    @allure.title("Invalid pic value")
    @pytest.mark.regression
    def test_invalid_pic(self, api_client, user_data, check):
        resp = api_client.create_user(user_data)
        check.assert_status_code(resp, 200)

        resp = api_client.update_user(user_data.login, pic="bad_value")

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_error_code(data, ErrorCode.VALIDATION_ERROR)
        check.assert_error_message_contains(data, Msg.PIC_INVALID)

    @allure.story("Profile Update")
    @allure.title("Facebook pic without username")
    @pytest.mark.regression
    def test_facebook_no_username(self, api_client, user_data, check):
        resp = api_client.create_user(user_data)
        check.assert_status_code(resp, 200)

        resp = api_client.update_user(user_data.login, pic="facebook")

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_error_code(data, ErrorCode.VALIDATION_ERROR)
        check.assert_error_message_contains(data, Msg.PIC_INVALID)


@allure.epic("FavQs API")
@allure.feature("User Management")
class TestUserRetrieval:
    """User retrieval tests."""

    @allure.story("User Info")
    @allure.title("Get without session")
    @pytest.mark.regression
    def test_get_without_session(self, created_user, check):
        _, user_data = created_user
        client = UserAPI()

        resp = client.get_user(user_data.login, authenticated=False)

        check.assert_status_code(resp, 200)
        data = resp.json()
        assert "error_code" in data or "login" in data

    @allure.story("User Info")
    @allure.title("Current user has account_details")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_account_details(self, created_user, check):
        client, user_data = created_user

        resp = client.get_user(user_data.login, authenticated=True)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_contains_key(data, "account_details")

        details = data["account_details"]
        assert details is not None
        check.assert_contains_key(details, "email")
        check.assert_equal(details["email"], user_data.email, "email")
        assert "private_favorites_count" in details
        assert isinstance(details["private_favorites_count"], int)

    @allure.story("User Info")
    @allure.title("Get other user public info")
    @pytest.mark.regression
    def test_other_user_public(self, created_user, check):
        client, _ = created_user
        target = "gose"

        resp = client.get_user(target, authenticated=True)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_contains_key(data, "login")
        check.assert_equal(data["login"], target, "login")

        for field in ["pic_url", "public_favorites_count", "followers", "following", "pro"]:
            assert field in data, f"{field} missing"

        assert isinstance(data.get("public_favorites_count"), int)
        assert isinstance(data.get("followers"), int)
        assert isinstance(data.get("following"), int)
        assert isinstance(data.get("pro"), bool)

        # Other users shouldn't have account_details
        assert "account_details" not in data or data.get("account_details") is None

    @allure.story("User Info")
    @allure.title("Non-existent user")
    @pytest.mark.regression
    def test_nonexistent(self, api_client):
        resp = api_client.get_user("nonexistent_12345")
        data = resp.json()
        assert resp.status_code in [200, 404] or "error" in str(data).lower()


@allure.epic("FavQs API")
@allure.feature("Session")
class TestSession:
    """Session tests."""

    @allure.story("Auth")
    @allure.title("Login/logout flow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_logout(self, api_client, user_data, check):
        resp = api_client.create_user(user_data)
        check.assert_status_code(resp, 200)

        resp = api_client.destroy_session()
        check.assert_status_code(resp, 200)

        resp = api_client.create_session(user_data.login, user_data.password)
        check.assert_status_code(resp, 200)
        check.assert_contains_key(resp.json(), "User-Token")

    @allure.story("Auth")
    @allure.title("Wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_wrong_password(self, created_user, check):
        _, user_data = created_user
        client = UserAPI()

        resp = client.create_session(user_data.login, "WrongPass123")

        check.assert_status_code(resp, 200)
        data = resp.json()
        assert "error_code" in data or "User-Token" not in data

    @allure.story("Auth")
    @allure.title("Non-existent user login")
    @pytest.mark.regression
    def test_nonexistent_login(self, api_client, check):
        resp = api_client.create_session("nobody_xyz", "Pass123")

        check.assert_status_code(resp, 200)
        data = resp.json()
        assert "error_code" in data or "User-Token" not in data

    @allure.story("Auth")
    @allure.title("Re-login gets new token")
    @pytest.mark.regression
    def test_relogin_new_token(self, created_user, check):
        client, user_data = created_user
        old_token = client.user_token

        resp = client.create_session(user_data.login, user_data.password)

        check.assert_status_code(resp, 200)
        data = resp.json()
        check.assert_contains_key(data, "User-Token")
        assert data["User-Token"] != old_token
