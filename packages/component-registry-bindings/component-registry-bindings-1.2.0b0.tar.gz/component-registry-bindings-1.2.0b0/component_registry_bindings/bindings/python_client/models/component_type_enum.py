from enum import Enum


class ComponentTypeEnum(str, Enum):
    CARGO = "CARGO"
    OCI = "OCI"
    GEM = "GEM"
    GENERIC = "GENERIC"
    GITHUB = "GITHUB"
    GOLANG = "GOLANG"
    MAVEN = "MAVEN"
    NPM = "NPM"
    RPMMOD = "RPMMOD"
    RPM = "RPM"
    PYPI = "PYPI"
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
