from enum import Enum


class BuildTypeEnum(str, Enum):
    BREW = "BREW"
    KOJI = "KOJI"
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
