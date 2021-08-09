
from package import Package


class Config:

    def __init__(self, base: str, token: str, packages: Package) -> None:
        self.base = base
        self.token = token
        self.packages = packages
