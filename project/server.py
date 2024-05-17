import logging
from contextlib import asynccontextmanager

import project.check_health_service
import project.deleteUserProfile_service
import project.get_version_service
import project.getDocumentation_service
import project.getHelloWorld_service
import project.getUserProfile_service
import project.listUsers_service
import project.loginUser_service
import project.registerUser_service
import project.updateUserProfile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hello worlld", lifespan=lifespan, description="create a hello world api"
)


@app.get(
    "/api/users/{userId}",
    response_model=project.getUserProfile_service.UserProfileResponseModel,
)
async def api_get_getUserProfile(
    userId: int,
) -> project.getUserProfile_service.UserProfileResponseModel | Response:
    """
    Retrieves the profile of the user identified by the provided userId. Returns user details excluding sensitive information like password.
    """
    try:
        res = project.getUserProfile_service.getUserProfile(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/version", response_model=project.get_version_service.VersionResponseModel)
async def api_get_get_version(
    request: project.get_version_service.VersionRequestModel,
) -> project.get_version_service.VersionResponseModel | Response:
    """
    This endpoint retrieves the current API version. It should be publicly accessible as it provides basic information about the API. The endpoint responds with a JSON object containing the 'version' key with the version of the API as its value. For instance, a typical response would be { 'version': '1.0.0' }.
    """
    try:
        res = project.get_version_service.get_version(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/users/login", response_model=project.loginUser_service.UserLoginResponseModel
)
async def api_post_loginUser(
    username: str, password: str
) -> project.loginUser_service.UserLoginResponseModel | Response:
    """
    Authenticates a user. Accepts username and password in the request body, verifies credentials, and returns a JWT token if successful.
    """
    try:
        res = project.loginUser_service.loginUser(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/hello", response_model=project.getHelloWorld_service.HelloWorldResponse)
async def api_get_getHelloWorld(
    request: project.getHelloWorld_service.HelloWorldRequest,
) -> project.getHelloWorld_service.HelloWorldResponse | Response:
    """
    This endpoint returns a simple 'Hello, World!' message. When a GET request is made to this endpoint, a plain text response with the content 'Hello, World!' will be returned.
    """
    try:
        res = project.getHelloWorld_service.getHelloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/docs", response_model=project.getDocumentation_service.GetDocsResponseModel)
async def api_get_getDocumentation(
    request: project.getDocumentation_service.GetDocsRequestModel,
) -> project.getDocumentation_service.GetDocsResponseModel | Response:
    """
    This route serves the API documentation for the 'hello worlld' product. When a GET request is made to this endpoint, it should return a comprehensive guide on how to use the API, including endpoint definitions, request/response formats, and any other pertinent information. The response should be in HTML or Markdown format, allowing users to easily navigate and understand the API functionalities.
    """
    try:
        res = await project.getDocumentation_service.getDocumentation(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/health", response_model=project.check_health_service.HealthCheckResponse)
async def api_get_check_health(
    request: project.check_health_service.HealthCheckRequest,
) -> project.check_health_service.HealthCheckResponse | Response:
    """
        This endpoint is called to check if the API is running properly. It will return a JSON object with the status of the service.

    Response:
    {
      "status": "UP"
    }

    How it works: The '/health' endpoint does not interact with other internal endpoints or external APIs. It simply checks if the server is up and running. If the server is functioning correctly, it returns a response with the status 'UP'. This endpoint is useful for monitoring and automated checks.
    """
    try:
        res = await project.check_health_service.check_health(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/users/register",
    response_model=project.registerUser_service.UserRegistrationResponse,
)
async def api_post_registerUser(
    password: str, username: str, email: str
) -> project.registerUser_service.UserRegistrationResponse | Response:
    """
    Registers a new user. Accepts user details (username, password, email) in the request body and creates a new user. Returns a success message along with the user ID.
    """
    try:
        res = await project.registerUser_service.registerUser(password, username, email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/users/{userId}",
    response_model=project.deleteUserProfile_service.DeleteUserResponseModel,
)
async def api_delete_deleteUserProfile(
    userId: int, Authorization: str
) -> project.deleteUserProfile_service.DeleteUserResponseModel | Response:
    """
    Deletes the user profile identified by the provided userId. This action should ensure that all user data is removed. Requires authentication and can be performed by the user themselves or an admin.
    """
    try:
        res = await project.deleteUserProfile_service.deleteUserProfile(
            userId, Authorization
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/api/users", response_model=project.listUsers_service.GetUsersResponse)
async def api_get_listUsers(
    role: str,
) -> project.listUsers_service.GetUsersResponse | Response:
    """
    Lists all users in the system. This route should return a list containing basic user details excluding sensitive information. This action is restricted to admin users.
    """
    try:
        res = await project.listUsers_service.listUsers(role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/users/{userId}",
    response_model=project.updateUserProfile_service.UpdateUserProfileResponse,
)
async def api_put_updateUserProfile(
    userId: int, username: str, email: str
) -> project.updateUserProfile_service.UpdateUserProfileResponse | Response:
    """
    Updates user profile information. The user can update fields such as username, and email. Requires authentication and the user can only update their own profile.
    """
    try:
        res = await project.updateUserProfile_service.updateUserProfile(
            userId, username, email
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
