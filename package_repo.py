from package import Package


class PackageRepo:

    def __init__(self, local, remote) -> None:
        self.local = local
        self.remote = remote

    def get(self, package: Package):
        if not self.local.exists(package):
            actionable = self.remote.get(package)
            if actionable:
                self.local.put(package, actionable)
        else:
            self.local.refresh(package)

    def put(self, package: Package):
        self.remote.put(package, self.local.package(package))
