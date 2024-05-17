import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class HealthCheckRequest(BaseModel):
    """
    The request model for the health check endpoint. Since this endpoint does not accept any input parameters, the Fields list is empty.
    """

    pass


class HealthCheckResponse(BaseModel):
    """
    The response model for the health check endpoint, returning a status message that indicates if the API service is running properly.
    """

    status: str


async def check_health(request: HealthCheckRequest) -> HealthCheckResponse:
    """
    This endpoint is called to check if the API is running properly. It will return a JSON object with the status of the service.

    Response:
    {
      "status": "UP"
    }

    How it works: The '/health' endpoint does not interact with other internal endpoints or external APIs. It simply checks if the server is up and running. If the server is functioning correctly, it returns a response with the status 'UP'. This endpoint is useful for monitoring and automated checks.

    Args:
    request (HealthCheckRequest): The request model for the health check endpoint. Since this endpoint does not accept any input parameters, the Fields list is empty.

    Returns:
    HealthCheckResponse: The response model for the health check endpoint, returning a status message that indicates if the API service is running properly.

    Example:
        request = HealthCheckRequest()
        response = await check_health(request)
        assert response.status == "UP"
    """
    await prisma.models.HealthCheck.prisma().create(
        data={"status": "UP", "checkedAt": datetime.datetime.now()}
    )
    response = HealthCheckResponse(status="UP")
    return response
