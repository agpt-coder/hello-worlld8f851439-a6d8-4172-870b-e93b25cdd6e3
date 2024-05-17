import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteUserResponseModel(BaseModel):
    """
    Response model for the deletion of a user which returns a success message and status.
    """

    status: str
    message: str


async def deleteUserProfile(userId: int, Authorization: str) -> DeleteUserResponseModel:
    """
    Deletes the user profile identified by the provided userId. This action should ensure that all user data is removed. Requires authentication and can be performed by the user themselves or an admin.

    Args:
        userId (int): The unique identifier of the user to be deleted.
        Authorization (str): Bearer authentication token for verifying user identity and role.

    Returns:
        DeleteUserResponseModel: Response model for the deletion of a user which returns a success message and status.

    Example:
        result = await deleteUserProfile(1, 'Bearer some_valid_token')
        > DeleteUserResponseModel(status='success', message='User deleted successfully.')
    """
    auth_token = Authorization.replace("Bearer ", "")
    auth_record = await prisma.models.Auth.prisma().find_first(
        where={"token": auth_token}
    )
    if not auth_record:
        return DeleteUserResponseModel(
            status="failure", message="Invalid authentication token."
        )
    requesting_user = await prisma.models.User.prisma().find_unique(
        where={"id": auth_record.userId}
    )
    if not requesting_user:
        return DeleteUserResponseModel(
            status="failure", message="Requesting user not found."
        )
    if requesting_user.role != prisma.enums.Role.Admin and requesting_user.id != userId:
        return DeleteUserResponseModel(status="failure", message="Unauthorized action.")
    await prisma.models.Auth.prisma().delete_many(where={"userId": userId})
    await prisma.models.User.prisma().delete(where={"id": userId})
    return DeleteUserResponseModel(
        status="success", message="User deleted successfully."
    )
