import prisma
import prisma.enums as enums
import prisma.models
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Model for the response after successfully registering a new user. It includes a success message and the user ID of the newly created user.
    """

    message: str
    user_id: int


async def registerUser(
    username: str, password: str, email: str
) -> UserRegistrationResponse:
    """
    Registers a new user. Accepts user details (username, password, email) in the request body and creates a new user.
    Returns a success message along with the user ID.

    Args:
        username (str): The username of the new user.
        password (str): The password for the new user's account.
        email (str): The email address of the new user.

    Returns:
        UserRegistrationResponse: Model for the response after successfully registering a new user. It includes a success message and the user ID of the newly created user.

    Example:
        response = await registerUser('john_doe', 'securepassword', 'john_doe@example.com')
        print(response.message)  # Output: 'User registered successfully.'
        print(response.user_id)  # Output: 1
    """
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": password, "role": enums.Role.User}
    )
    return UserRegistrationResponse(
        message="User registered successfully.", user_id=new_user.id
    )
