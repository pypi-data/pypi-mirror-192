from enum import Enum


class V1ComponentsListType(str, Enum):
    CARGO = "CARGO"
    GEM = "GEM"
    GENERIC = "GENERIC"
    GITHUB = "GITHUB"
    GOLANG = "GOLANG"
    MAVEN = "MAVEN"
    NPM = "NPM"
    OCI = "OCI"
    PYPI = "PYPI"
    RPM = "RPM"
    RPMMOD = "RPMMOD"

    def __str__(self) -> str:
        return str(self.value)
