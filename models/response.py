"""API response models."""
from dataclasses import dataclass
from typing import Optional, Union

from api.error_codes import ErrorCode


@dataclass
class ErrorResponse:
    """API error response."""
    error_code: int
    message: Union[str, dict]

    @classmethod
    def from_dict(cls, data: dict) -> Optional["ErrorResponse"]:
        if "error_code" not in data:
            return None
        return cls(error_code=data["error_code"], message=data.get("message", ""))

    @property
    def is_validation_error(self) -> bool:
        return self.error_code == ErrorCode.VALIDATION_ERROR

    @property
    def message_str(self) -> str:
        if isinstance(self.message, str):
            return self.message
        if isinstance(self.message, dict):
            parts = []
            for field, errors in self.message.items():
                errs = errors if isinstance(errors, list) else [errors]
                parts.extend(f"{field}: {e}" for e in errs)
            return "; ".join(parts)
        return str(self.message)

    def has_field(self, field: str) -> bool:
        if isinstance(self.message, dict):
            return field.lower() in [k.lower() for k in self.message.keys()]
        return field.lower() in self.message_str.lower()

    def contains(self, text: str) -> bool:
        return text.lower() in self.message_str.lower()
