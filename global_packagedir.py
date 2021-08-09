from os import path
import os
import tarfile


class GlobalPackagedir:

    TARDIR = '.cache'

    def __init__(self, global_base) -> None:
        self.cachedir = path.join(global_base, self.TARDIR)

    def exists(self, package):
        return path.exists(path.join(self.cachedir, package.filename))

    def put(self, package, streamed):
        if not path.exists(self.cachedir):
            os.makedirs(self.cachedir)

        cache_file_path = path.join(self.cachedir, package.filename)

        with open(cache_file_path, 'wb') as f:
            streamed(f.write)

    def package(self, package):
        if not path.exists(self.cachedir):
            os.makedirs(self.cachedir)

        with tarfile.open(path.join(self.cachedir, package.filename), 'w:gz') as tar:
            for f in os.listdir(package.src):
                tar.add(path.join(package.src, f))
        return path.join(self.cachedir, package.filename)

    def get_path(self, package):
        return path.join(self.cachedir, package.filename) if self.exists(package) else None
