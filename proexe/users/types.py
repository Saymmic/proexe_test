from typing import Protocol


class UserProtocol(Protocol):
    username: str
    email: str
    password: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
