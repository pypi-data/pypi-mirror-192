import json
from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseSettings

from databricks_access_layer.aws.secretmanager import get_secret


class SnowflakeCredentials(BaseSettings):
    """
    A Class used to define the default credentials for accessing Snowflake
    """

    username: str
    password: str
    account: str
    role: str
    warehouse: str
    region: str
    database: str
    db_schema: Optional[str] = None

    class Config:
        env_prefix = "dal_"


class AuthProvider(ABC):
    """
    A Class used to define an authentication provider
    """

    @abstractmethod
    def get_credentials(self) -> SnowflakeCredentials:
        """Class method to obtain the credentials"""
        pass


class SecretsManagerProvider(AuthProvider):
    def __init__(self, secret_name: str) -> None:
        self.secret_name = secret_name

    def get_credentials(self) -> SnowflakeCredentials:
        """Class method to return the credentials"""
        credentials = get_secret(self.secret_name)
        return SnowflakeCredentials(**credentials)


class DatabricksSecretsProvider(AuthProvider):
    """Class method to set de credentials from databricks provider"""

    def __init__(self, dbutils, scope: str = "data", key: str = "snowflake") -> None:  # type: ignore
        self.dbutils = dbutils
        self.scope = scope
        self.key = key

    def get_credentials(self) -> SnowflakeCredentials:
        snowflake_secrets = self.dbutils.secrets.get(scope=self.scope, key=self.key)
        credentials = json.loads(snowflake_secrets)
        return SnowflakeCredentials(**credentials)
