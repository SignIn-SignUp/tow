import gitlab

from .package import Package


class GitLabController:

    def __init__(self, base: str, token: str) -> None:
        self.gl = gitlab.Gitlab(base, private_token=token)

    def get(self, package: Package):
        return lambda f: self.gl.projects.get(package.project, lazy=True).generic_packages.download(
            package_name=package.name,
            package_version=package.version,
            file_name=package.filename,
            streamed=True,
            action=f
        )

    def put(self, package: Package, path: str):
        self.gl.projects.get(package.project, lazy=True).generic_packages.upload(
            package_name=package.name,
            package_version=package.version,
            file_name=package.filename,
            path=path
        )
