import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class UserPasswordCredentials:
    username: str
    password: str


class NoCredentialsError(Exception): ...


def load_credentials() -> UserPasswordCredentials:
    env_file = Path(".env")

    if not env_file.exists():
        raise NoCredentialsError(
            "No .env file found. Please create one based on sample.env with your RideWithGPS email and password."
            "see https://ridewithgps.com/api for more information."
        )

    load_dotenv(env_file)

    username = os.getenv("RIDEWITHGPS_USERNAME")
    password = os.getenv("RIDEWITHGPS_PASSWORD")

    if not username:
        raise ValueError("Missing required environment variable: RIDEWITHGPS_USERNAME")
    if not password:
        raise ValueError("Missing required environment variable: RIDEWITHGPS_PASSWORD")

    return UserPasswordCredentials(username=username, password=password)
