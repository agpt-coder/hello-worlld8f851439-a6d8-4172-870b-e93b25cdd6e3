from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserDetail(BaseModel):
    """
    Basic details of a user excluding sensitive information.
    """

    id: int
    email: str
    role: prisma.enums.Role


class GetUsersResponse(BaseModel):
    """
    Response model for listing all users. Contains the list of users with basic details excluding sensitive information.
    """

    users: List[UserDetail]


async def listUsers(role: str) -> GetUsersResponse:
    """
    Lists all users in the system. This route should return a list containing basic user details excluding sensitive information. This action is restricted to admin users.

    Args:
    role (str): The role of the requesting user to validate permission. This should be 'admin'.

    Returns:
    GetUsersResponse: Response model for listing all users. Contains the list of users with basic details excluding sensitive information.

    Example:
        response = await listUsers('admin')
        > GetUsersResponse(users=[UserDetail(id=1, email='user1@example.com', role='User'), ...])
    """
    if role.lower() != "admin":
        raise PermissionError("Access denied: Admin role required.")
    users = await prisma.models.User.prisma().find_many()
    user_details = [
        UserDetail(id=user.id, email=user.email, role=user.role) for user in users
    ]
    return GetUsersResponse(users=user_details)
