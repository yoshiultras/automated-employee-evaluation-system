import os
from dataclasses import dataclass, field

from jinja2 import Environment, FileSystemLoader


def get_from_env(name) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError("Could not find environment variable %s" % name)
    return value


@dataclass
class PostgresSettings:
    host: str = field(init=False)
    port: int = field(init=False)
    user: str = field(init=False)
    password: str = field(init=False)
    database: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self.host = get_from_env("POSTGRES_HOST")
        self.port = int(get_from_env("POSTGRES_PORT"))
        self.user = get_from_env("POSTGRES_USER")
        self.password = get_from_env("POSTGRES_PASSWORD")
        self.database = get_from_env("POSTGRES_DB")
        self.url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(  # noqa E501
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


@dataclass
class Settings:
    domain: str = field(init=False)
    client_domain: str = field(init=False)
    https: bool = field(init=False)

    host: str = field(init=False)
    port: int = field(init=False)
    site_api_path: str = field(init=False)
    docs_url: str = field(init=False)

    database: PostgresSettings = field(
        init=False,
        default_factory=PostgresSettings,
    )

    def __post_init__(self):
        self.domain = get_from_env("DOMAIN")
        self.client_domain = get_from_env("CLIENT_DOMAIN")
        self.https = get_from_env("HTTPS") == "true"
        self.http_protocol = "https" if self.https else "http"

        self.host = get_from_env("BACKEND_HOST")
        self.port = int(get_from_env("BACKEND_PORT"))
        self.site_api_path = get_from_env("SITE_API_PATH")
        self.docs_url = get_from_env("DOCS_URL")
