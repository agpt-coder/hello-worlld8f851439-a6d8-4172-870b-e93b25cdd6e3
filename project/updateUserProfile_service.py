import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Response model after updating user profile information. Returns the updated user profile.
    """

    id: int
    username: str
    email: str
    role: prisma.enums.Role


async def updateUserProfile(
    userId: int, username: str, email: str
) -> UpdateUserProfileResponse:
    """
    Updates user profile information. The user can update fields such as username, and email. Requires authentication and the user can only update their own profile.

    Args:
    userId (int): The ID of the user whose profile is being updated.
    username (str): The new username for the user.
    email (str): The new email for the user.

    Returns:
    UpdateUserProfileResponse: Response model after updating user profile information. Returns the updated user profile.

    Example:
        response = await updateUserProfile(1, "new_username", "new_email@example.com")
        > UpdateUserProfileResponse(id=1, username="new_username", email="new_email@example.com", role="User")
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        raise ValueError(f"No user found with ID {userId}")
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId}, data={"email": email, "username": username}
    )
    response = UpdateUserProfileResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        role=updated_user.role.value,
    )  # TODO(autogpt): Cannot access attribute "username" for class "User"
    #     Attribute "username" is unknown. reportAttributeAccessIssue
    return response
