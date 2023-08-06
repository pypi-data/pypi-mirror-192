from enum import Enum


class ChannelTypeEnum(str, Enum):
    CDN_REPO = "CDN_REPO"
    CONTAINER_REGISTRY = "CONTAINER_REGISTRY"
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
