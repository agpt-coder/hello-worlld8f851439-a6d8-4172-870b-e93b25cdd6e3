from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetDocsRequestModel(BaseModel):
    """
    This request model represents the GET request to the /docs endpoint. Since it's a simple GET request to retrieve documentation, there are no request parameters needed.
    """

    pass


class GetDocsResponseModel(BaseModel):
    """
    This response model represents the structure of the response for the docs endpoint, which will be either in HTML or Markdown format, based on content stored in the 'Documentation' database model.
    """

    content: str
    updatedAt: datetime


async def getDocumentation(request: GetDocsRequestModel) -> GetDocsResponseModel:
    """
    This route serves the API documentation for the 'hello worlld' product. When a GET request is made to this endpoint, it should return a comprehensive guide on how to use the API, including endpoint definitions, request/response formats, and any other pertinent information. The response should be in HTML or Markdown format, allowing users to easily navigate and understand the API functionalities.

    Args:
    request (GetDocsRequestModel): This request model represents the GET request to the /docs endpoint. Since it's a simple GET request to retrieve documentation, there are no request parameters needed.

    Returns:
    GetDocsResponseModel: This response model represents the structure of the response for the docs endpoint, which will be either in HTML or Markdown format, based on content stored in the 'Documentation' database model.

    Example:
    request = GetDocsRequestModel()
    response = await getDocumentation(request)
    """
    documentation: Optional[
        prisma.models.Documentation
    ] = await prisma.models.Documentation.prisma().find_first(
        order={"updatedAt": "desc"}
    )
    if not documentation:
        return GetDocsResponseModel(content="", updatedAt=datetime.utcnow())
    return GetDocsResponseModel(
        content=documentation.content, updatedAt=documentation.updatedAt
    )
