from enum import Enum


class V1ChannelsListType(str, Enum):
    CDN_REPO = "CDN_REPO"
    CONTAINER_REGISTRY = "CONTAINER_REGISTRY"

    def __str__(self) -> str:
        return str(self.value)
