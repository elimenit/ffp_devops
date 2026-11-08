"""Calls the API for Users 
"""
from schemas.user import UserBase, UserGet, UserPost
import requests
from requests import Response


def post_create_user(user: UserPost, url: str) -> tuple[int, dict[str, str]]:
    """
    return: (status_code, json response)
    """
    response: Response = requests.post(url=url, json=user.model_dump(exclude_none=True))
    return response.status_code, response.json()
