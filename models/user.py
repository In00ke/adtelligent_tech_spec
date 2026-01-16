"""User models."""
from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class UserData:
    """User data for requests."""
    login: str
    email: str
    password: str = "TestPass123"

    @classmethod
    def generate(cls, prefix: str = "testuser"):
        uid = uuid.uuid4().hex[:8]
        return cls(login=f"{prefix}_{uid}", email=f"{prefix}_{uid}@test.com")

    def to_dict(self) -> dict:
        return {"login": self.login, "email": self.email, "password": self.password}


@dataclass
class AccountDetails:
    """User account details."""
    email: str
    private_favorites_count: int = 0

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            email=data.get("email", ""),
            private_favorites_count=data.get("private_favorites_count", 0)
        )


@dataclass
class UserResponse:
    """User API response."""
    login: str
    user_token: Optional[str] = None
    pic_url: Optional[str] = None
    public_favorites_count: int = 0
    followers: int = 0
    following: int = 0
    pro: bool = False
    account_details: Optional[AccountDetails] = None

    @classmethod
    def from_dict(cls, data: dict):
        details = None
        if "account_details" in data:
            details = AccountDetails.from_dict(data["account_details"])

        return cls(
            login=data.get("login", ""),
            user_token=data.get("User-Token"),
            pic_url=data.get("pic_url"),
            public_favorites_count=data.get("public_favorites_count", 0),
            followers=data.get("followers", 0),
            following=data.get("following", 0),
            pro=data.get("pro", False),
            account_details=details
        )

    @property
    def email(self):
        return self.account_details.email if self.account_details else None
