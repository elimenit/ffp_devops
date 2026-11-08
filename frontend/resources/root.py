"""Endpoints root for Frontend
"""

import requests

from constants import URL_BACKEND


def get_root():
    """Return call API Rest Backend"""

    response = requests.get(url=URL_BACKEND)
    if response.status_code == 200:
        return response.json()

    raise Exception("Fallo la solicitud!")
