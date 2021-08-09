

class PackageController:

    def __init__(self, project_repo, global_repo) -> None:
        self.local_ = project_repo
        self.global_ = global_repo

    def exists(self, package):
        return self.global_.exists(package)

    def put(self, package, streamed):
        self.global_.put(package, streamed)
        self.local_.put(package, self.global_.get_path(package))

    def refresh(self, package):
        self.local_.put(package, self.global_.get_path(package))

    def package(self, package):
        return self.global_.package(package)
