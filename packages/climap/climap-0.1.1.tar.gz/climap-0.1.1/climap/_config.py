from dataclasses import dataclass
from typing import TypedDict


class ClientArgs(TypedDict):
    host: str
    port: int


@dataclass(frozen=True)
class Config:
    """An encapsulation of the runtime configuration."""

    host: str
    user: str
    password: str
    port: int = 993
    ssl: bool = True

    @property
    def client_args(self) -> ClientArgs:
        return {
            "host": self.host,
            "port": self.port,
        }
