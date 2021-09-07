from os import path
import os
import tarfile


class LocalPackagedir:

    def __init__(self, base) -> None:
        self.base = base
        self.basedir = path.join(os.getcwd(), base)

    def exists(self, package):
        return path.exists(path.join(self.basedir, package.name, package.version))

    def put(self, package, path):
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        with tarfile.open(path) as f:
            f.extractall(
                os.path.join(self.basedir, package.name, package.version)
            )
