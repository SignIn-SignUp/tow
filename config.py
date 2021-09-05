
from settings import Settings
from package import Package


class Config:

    def __init__(self, base: str, token: str, packages: Package, settings: Settings) -> None:
        self.base = base
        self.token = token
        self.packages = packages
        self.settings = settings
