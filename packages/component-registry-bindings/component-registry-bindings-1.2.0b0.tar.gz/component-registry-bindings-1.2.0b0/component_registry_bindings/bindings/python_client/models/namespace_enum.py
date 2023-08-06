from enum import Enum


class NamespaceEnum(str, Enum):
    UPSTREAM = "UPSTREAM"
    REDHAT = "REDHAT"
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
