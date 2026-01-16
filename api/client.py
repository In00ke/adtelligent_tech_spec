"""Base API client."""
import allure
import requests
from config import BASE_URL, get_base_headers, get_auth_headers
from utils.logger import get_logger, log_request, log_response


class APIClient:
    """Base HTTP client."""

    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.user_token = None
        self.logger = get_logger(self.__class__.__name__)

    def _get_headers(self, authenticated=False):
        if authenticated and self.user_token:
            return get_auth_headers(self.user_token)
        return get_base_headers()

    def _request(self, method, endpoint, data=None, authenticated=False, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(authenticated)

        log_request(self.logger, method, url, headers, data)

        with allure.step(f"{method} {endpoint}"):
            resp = self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                **kwargs
            )
            log_response(self.logger, resp)

            allure.attach(
                f"URL: {url}\nMethod: {method}\nStatus: {resp.status_code}",
                name="Request",
                attachment_type=allure.attachment_type.TEXT
            )

        return resp

    def get(self, endpoint, authenticated=False, **kwargs):
        return self._request("GET", endpoint, authenticated=authenticated, **kwargs)

    def post(self, endpoint, data=None, authenticated=False, **kwargs):
        return self._request("POST", endpoint, data=data, authenticated=authenticated, **kwargs)

    def put(self, endpoint, data=None, authenticated=False, **kwargs):
        return self._request("PUT", endpoint, data=data, authenticated=authenticated, **kwargs)

    def delete(self, endpoint, authenticated=False, **kwargs):
        return self._request("DELETE", endpoint, authenticated=authenticated, **kwargs)

    def set_user_token(self, token):
        self.user_token = token
        self.logger.info("Token set")
