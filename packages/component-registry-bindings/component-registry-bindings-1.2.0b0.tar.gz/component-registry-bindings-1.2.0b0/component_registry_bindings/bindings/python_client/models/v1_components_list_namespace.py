from enum import Enum


class V1ComponentsListNamespace(str, Enum):
    REDHAT = "REDHAT"
    UPSTREAM = "UPSTREAM"

    def __str__(self) -> str:
        return str(self.value)
