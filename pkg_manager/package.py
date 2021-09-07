
class Package:

    def __init__(self, name: str, version: str, filename: str, project: str, src: str = None) -> None:
        self.name = name
        self.version = version
        self.filename = filename
        self.project = project
        self.src = src
