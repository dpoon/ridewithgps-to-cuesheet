from dataclasses import dataclass

import requests

from .logger import logger


@dataclass
class AuthToken:
    api_key: str
    token: str


def authenticate(email: str, password: str, session_name: str) -> AuthToken:
    logger.debug(f"Authenticating with RideWithGPS and session name: {session_name}")
    auth_url = "https://ridewithgps.com/users/current.json"
    response = requests.get(
        auth_url,
        params={"version": str(2), "api_key": session_name, "email": email, "password": password},
        timeout=10,
    )
    response.raise_for_status()

    user_data = response.json()
    auth_token = user_data.get("user", {}).get("auth_token")

    if not auth_token:
        raise ValueError("Failed to retrieve authentication token from RideWithGPS")

    logger.debug("Authenticated successfully. Validating auth")
    requests.get(auth_url, params={"version": str(2), "auth_token": auth_token, "api_key": session_name}, timeout=10)

    return AuthToken(token=auth_token, api_key=session_name)


def download_csv_content(route_id: str, auth_token: AuthToken) -> str:
    logger.debug(f"Downloading CSV content for route ID: {route_id}")
    response = requests.get(
        f"https://ridewithgps.com/routes/{route_id}.csv",
        params={"version": str(2), "auth_token": auth_token.token, "api_key": auth_token.api_key},
        timeout=10,
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    return response.text
