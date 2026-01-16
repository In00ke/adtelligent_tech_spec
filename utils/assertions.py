"""Assertion helpers for API tests."""
from typing import Any, Union

import allure
from requests import Response

from api.error_codes import ErrorCode, Msg


class AssertionHelper:
    """Common assertions with Allure integration."""

    @staticmethod
    def assert_status_code(response: Response, expected: int, msg: str = ""):
        with allure.step(f"Check status code is {expected}"):
            actual = response.status_code
            err = f"Expected {expected}, got {actual}"
            if msg:
                err = f"{msg}: {err}"
            if actual != expected:
                err += f"\nResponse: {response.text}"
            assert actual == expected, err

    @staticmethod
    def assert_equal(actual: Any, expected: Any, name: str):
        with allure.step(f"Check {name} == '{expected}'"):
            assert actual == expected, f"{name}: expected '{expected}', got '{actual}'"

    @staticmethod
    def assert_not_none(value: Any, name: str):
        with allure.step(f"Check {name} is present"):
            assert value is not None, f"{name} is None"

    @staticmethod
    def assert_contains_key(data: dict, key: str, msg: str = ""):
        with allure.step(f"Check '{key}' in response"):
            err = f"'{key}' not found"
            if msg:
                err = f"{msg}: {err}"
            assert key in data, err

    @staticmethod
    def assert_error_code(data: dict, expected: Union[int, ErrorCode]):
        code = int(expected)
        with allure.step(f"Check error_code == {code}"):
            assert "error_code" in data, f"No error_code: {data}"
            assert data["error_code"] == code, f"Expected {code}, got {data['error_code']}"

    @staticmethod
    def _msg_to_str(message) -> str:
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            parts = []
            for field, errors in message.items():
                errs = errors if isinstance(errors, list) else [errors]
                parts.extend(f"{field}: {e}" for e in errs)
            return "; ".join(parts)
        return str(message)

    @staticmethod
    def assert_error_message_contains(data: dict, text: str):
        with allure.step(f"Check message contains '{text}'"):
            assert "message" in data, f"No message: {data}"
            msg_str = AssertionHelper._msg_to_str(data["message"])
            assert text.lower() in msg_str.lower(), f"'{text}' not in '{msg_str}'"

    @staticmethod
    def assert_validation_error(data: dict, field: str):
        with allure.step(f"Check validation error for '{field}'"):
            assert "error_code" in data, f"No error_code: {data}"
            assert data["error_code"] == ErrorCode.VALIDATION_ERROR, \
                f"Expected {ErrorCode.VALIDATION_ERROR}, got {data['error_code']}"
            assert "message" in data, f"No message: {data}"

            msg = data["message"]
            if isinstance(msg, dict):
                assert field.lower() in [k.lower() for k in msg.keys()], \
                    f"'{field}' not in {list(msg.keys())}"
            else:
                assert field.lower() in str(msg).lower(), f"'{field}' not in '{msg}'"

    @staticmethod
    def assert_field_error(data: dict, field: str, error: str):
        with allure.step(f"Check '{field}' error contains '{error}'"):
            assert "message" in data, f"No message: {data}"
            msg = data["message"]

            if isinstance(msg, dict):
                assert field in msg, f"'{field}' not in {list(msg.keys())}"
                errs = msg[field]
                err_str = " ".join(errs) if isinstance(errs, list) else str(errs)
                assert error.lower() in err_str.lower(), f"'{error}' not in {errs}"
            else:
                assert error.lower() in str(msg).lower(), f"'{error}' not in '{msg}'"

    @staticmethod
    def assert_success_message(data: dict, text: str = Msg.UPDATED):
        with allure.step(f"Check success message"):
            assert "message" in data, f"No message: {data}"
            assert "error_code" not in data, f"Got error: {data}"
            assert text.lower() in data["message"].lower(), \
                f"'{text}' not in '{data['message']}'"
