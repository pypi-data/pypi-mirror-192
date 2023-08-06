from typing import Optional, List

from vulcan.core.user.schemas.user import LoginResponseSchema, GetUserListResponseSchema
from vulcan.core.exceptions import (
    NotImplementException,
)


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[GetUserListResponseSchema]:
        raise NotImplementException("UserService.get_user_list")

    async def is_admin(self, user_id: int) -> bool:
        raise NotImplementException("UserService.is_admin")

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        raise NotImplementException("UserService.login")
